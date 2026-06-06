const STAGES = [
    "Upload Complete",
    "Extracting Text",
    "Generating Summary",
    "Extracting Decisions",
    "Extracting Actions",
    "Extracting Risks",
    "Updating Timeline"
];

const activeJobs = new Map();

function initProjectForm() {
    const projectForm = document.getElementById("project-form");
    if (!projectForm) return;
    projectForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(projectForm);
        const response = await fetch("/api/projects", { method: "POST", body: formData });
        if (!response.ok) {
            return;
        }
        window.location.reload();
    });
}

function initTabs() {
    document.querySelectorAll("[data-tab-group]").forEach((group) => {
        const buttons = group.querySelectorAll(".tab-button");
        buttons.forEach((button) => {
            button.addEventListener("click", () => {
                const target = button.dataset.tabTarget;
                buttons.forEach((item) => item.classList.toggle("active", item === button));
                document.querySelectorAll("[data-tab-panel]").forEach((panel) => {
                    panel.classList.toggle("active", panel.dataset.tabPanel === target);
                });
            });
        });
    });
}

function initSearch() {
    const searchForm = document.getElementById("search-form");
    if (!searchForm) return;
    searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const params = new URLSearchParams(new FormData(searchForm));
        const response = await fetch(`/api/search?${params.toString()}`);
        const data = await response.json();
        const container = document.getElementById("search-results");
        container.innerHTML = "";
        if (!data.results.length) {
            container.innerHTML = "<p class='empty-state'>No results found.</p>";
            return;
        }
        data.results.forEach((item) => {
            const row = document.createElement("div");
            row.className = "search-result";
            row.innerHTML = `
                <div><strong>${item.result_type}</strong></div>
                <div>${item.project} | <a href="${item.link}">${item.document}</a></div>
                <p>${item.snippet}</p>
            `;
            container.appendChild(row);
        });
    });
}

function initUploadPanels() {
    document.querySelectorAll(".upload-panel").forEach((panel) => {
        const dropzone = panel.querySelector(".dropzone");
        const input = panel.querySelector(".file-input");
        const list = panel.querySelector(".selected-files");
        const trigger = panel.querySelector(".upload-trigger");
        const status = panel.querySelector(".status");
        let selectedFiles = [];

        const renderFiles = () => {
            list.innerHTML = "";
            if (!selectedFiles.length) {
                list.innerHTML = "<p class='empty-state'>No files selected.</p>";
                return;
            }
            selectedFiles.forEach((file, index) => {
                const row = document.createElement("div");
                row.className = "file-row";
                row.dataset.fileIndex = String(index);
                row.innerHTML = `
                    <div class="file-row-head">
                        <strong>${file.name}</strong>
                        <span>${Math.ceil(file.size / 1024)} KB</span>
                    </div>
                    <div class="progress-track"><div class="progress-bar"></div></div>
                    <div class="subtle file-status">Ready for upload</div>
                `;
                list.appendChild(row);
            });
        };

        const setFiles = (files) => {
            selectedFiles = Array.from(files).filter((file) => /\.(pdf|docx|txt|md)$/i.test(file.name));
            renderFiles();
        };

        dropzone.addEventListener("dragover", (event) => {
            event.preventDefault();
            dropzone.classList.add("dragover");
        });

        dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
        dropzone.addEventListener("drop", (event) => {
            event.preventDefault();
            dropzone.classList.remove("dragover");
            setFiles(event.dataTransfer.files);
        });

        input.addEventListener("change", () => setFiles(input.files));

        trigger.addEventListener("click", async () => {
            if (!selectedFiles.length) {
                status.textContent = "Select at least one supported file.";
                return;
            }
            status.textContent = "Uploading files...";
            showOverlay();
            for (let i = 0; i < selectedFiles.length; i += 1) {
                await uploadSingleFile(panel.dataset.projectId, selectedFiles[i], i, list, status);
            }
            status.textContent = "Uploads submitted. Background processing is running.";
        });

        renderFiles();
    });
}

function uploadSingleFile(projectId, file, index, list, statusLabel) {
    return new Promise((resolve) => {
        const row = list.querySelector(`[data-file-index="${index}"]`);
        const progressBar = row?.querySelector(".progress-bar");
        const fileStatus = row?.querySelector(".file-status");
        const formData = new FormData();
        formData.append("files", file);

        const xhr = new XMLHttpRequest();
        xhr.open("POST", `/api/projects/${projectId}/documents`);
        xhr.upload.addEventListener("progress", (event) => {
            if (!event.lengthComputable || !progressBar) return;
            const percent = Math.round((event.loaded / event.total) * 100);
            progressBar.style.width = `${percent}%`;
            if (fileStatus) fileStatus.textContent = `Upload ${percent}%`;
        });
        xhr.onreadystatechange = () => {
            if (xhr.readyState !== XMLHttpRequest.DONE) return;
            if (xhr.status >= 200 && xhr.status < 300) {
                const payload = JSON.parse(xhr.responseText);
                const item = payload.items[0];
                if (item.skipped) {
                    if (fileStatus) fileStatus.textContent = "Already processed. Existing document reused.";
                } else {
                    if (fileStatus) fileStatus.textContent = "Upload complete. Processing started.";
                    registerJob(item.job_id, item.filename, item.document_id || item.id);
                }
                resolve();
                return;
            }
            if (fileStatus) fileStatus.textContent = "Upload failed.";
            statusLabel.textContent = "One or more files failed to upload.";
            resolve();
        };
        xhr.send(formData);
    });
}

function initOverlay() {
    const close = document.getElementById("overlay-close");
    if (close) {
        close.addEventListener("click", () => {
            document.getElementById("processing-overlay").classList.add("hidden");
        });
    }
}

function showOverlay() {
    document.getElementById("processing-overlay").classList.remove("hidden");
}

function registerJob(jobId, filename, documentId) {
    if (!jobId) return;
    activeJobs.set(jobId, { filename, documentId, status: "processing", stage: "Upload Complete", progress: 10 });
    renderJobs();
    pollJob(jobId);
}

async function pollJob(jobId) {
    const entry = activeJobs.get(jobId);
    if (!entry) return;
    try {
        const response = await fetch(`/api/jobs/${jobId}`);
        const data = await response.json();
        activeJobs.set(jobId, { ...entry, ...data });
        renderJobs();
        if (data.status === "processing" || data.status === "queued") {
            window.setTimeout(() => pollJob(jobId), 1500);
            return;
        }
        if (allJobsDone()) {
            window.setTimeout(() => {
                document.getElementById("processing-overlay").classList.add("hidden");
                window.location.reload();
            }, 1000);
        }
    } catch (error) {
        window.setTimeout(() => pollJob(jobId), 2500);
    }
}

function renderJobs() {
    const container = document.getElementById("overlay-jobs");
    if (!container) return;
    container.innerHTML = "";
    activeJobs.forEach((job, jobId) => {
        const card = document.createElement("div");
        card.className = "job-card";
        const steps = STAGES.map((stage) => {
            const stageIndex = STAGES.indexOf(stage);
            const currentIndex = STAGES.indexOf(job.stage);
            let className = "";
            let icon = "[ ]";
            if (job.status === "complete" || stageIndex < currentIndex) {
                className = "done";
                icon = "[✓]";
            }
            if (stage === job.stage && job.status !== "complete" && job.status !== "failed") {
                className = "active";
            }
            if (job.status === "failed" && stage === job.stage) {
                className = "active";
            }
            return `<li class="${className}">${icon} ${stage}</li>`;
        }).join("");
        card.innerHTML = `
            <div class="job-head">
                <strong>${job.filename}</strong>
                <span>${job.stage} | ${job.progress}% | ${job.status}</span>
            </div>
            <div class="progress-track"><div class="progress-bar" style="width:${job.progress}%"></div></div>
            <ul class="step-list">${steps}</ul>
            ${job.error_message ? `<p class="empty-state">${job.error_message}</p>` : ""}
        `;
        container.appendChild(card);
    });
}

function allJobsDone() {
    return [...activeJobs.values()].every((job) => job.status === "complete" || job.status === "failed");
}

function initResummarize() {
    document.querySelectorAll("[data-resummarize-id]").forEach((button) => {
        button.addEventListener("click", async () => {
            showOverlay();
            const response = await fetch(`/api/documents/${button.dataset.resummarizeId}/summarize`, { method: "POST" });
            const data = await response.json();
            registerJob(data.job_id, `Document ${data.document_id}`, data.document_id);
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initProjectForm();
    initTabs();
    initSearch();
    initUploadPanels();
    initOverlay();
    initResummarize();
});
