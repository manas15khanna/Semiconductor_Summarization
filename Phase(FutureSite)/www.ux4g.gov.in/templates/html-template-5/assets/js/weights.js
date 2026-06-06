/*
* UX4G v1.0.0 (https://doc.ux4g.gov.in/)
* Copyright 2024 The UX4G Authors
* Copyright 2024 NeGD, MeitY.
* Licensed under MIT. 
 */

// Exclude Widgets text, links, Images on widgets click

function isExcludedElement(element) {
    // Check if the element is inside #uw-main or has class .uwaw-features__item__name
    if (
          element.closest('#uw-main') ||
          element.classList.contains('uwaw-features__item__name') ||
          element.classList.contains('ux4g-text-spacing') ||
          element.classList.contains('feature-image') ||
          element.classList.contains('icon_global') ||
          element.classList.contains('copyright-text') ||
          element.classList.contains('ux4g-copy')
        ) {
            return true;
        }
    
        // Exclude script and svg elements
        if (element.tagName === 'SCRIPT' || element.tagName === 'DIV' || element.tagName === 'LINK'
       || element.tagName === 'HTML'
       || element.tagName === 'HEAD'
       || element.tagName === 'BODY'
        || (element.tagName === 'svg' && element.namespaceURI === 'http://www.w3.org/2000/svg')) {
            return true;
        }
    
        return false;
    }
    
    
    /***************************************************************************************************/
  
  
  // ******************************************************************************* //
  
  // Bigger & Smaller text script
  
  function handleFontSizes(btnId, featureItemId, featureStepsId, tickIconId, increase, btn) {
    var Storageclick = btn + '-clickCount';
    var ButtonStorageClick = btn + '-buttonClicked';
    var SizeStorage = btn + '-size';
    var clickCount = 0;
    var addsize = 0;
  
    // Check local storage for previous state
      var localStorageClickCount = localStorage.getItem(Storageclick);
      if (localStorageClickCount) {
        clickCount = parseInt(localStorageClickCount, 10);
      }
  
    document.addEventListener('DOMContentLoaded', function() { 
  
      var featureItem = document.getElementById(featureItemId);
      var featureSteps = document.getElementById(featureStepsId);
      var tickIcon = document.getElementById(tickIconId);
  
      // Get Storage Items
      var FontSizeBtnState = JSON.parse(localStorage.getItem(ButtonStorageClick));
      var FontSizeClickState = JSON.parse(localStorage.getItem(Storageclick));
      // var FontSizeState = localStorage.getItem(SizeStorage);
      var FontSizeStateBigger = localStorage.getItem('bt-size');
      var FontSizeStateSmaller = localStorage.getItem('st-size');
  
  
      if (FontSizeBtnState) {
  
        featureItem.classList.add('feature-active');
        featureSteps.classList.add('featureSteps-visible');
        tickIcon.style.display = 'inline-block';
  
        // Add step span tags dynamically
        var StoragestepsHTML = '';
        for (var i = 0; i < 4; i++) {
          StoragestepsHTML += '<span class="' + (i < FontSizeClickState ? 'active step uwaw-features__step' : 'step uwaw-features__step') + '"></span>';
        }
        featureSteps.innerHTML = StoragestepsHTML;
  
        if (FontSizeStateBigger != 0) {
          document.getElementById('btn-small-text').disabled = true;
          var elements = document.querySelectorAll('*:not(.uw-widget-custom-trigger, .uw-widget-custom-trigger span)');
          elements.forEach(function(element) {
          // Exclude elements inside #uw-main and with class .uwaw-features__item__name
          if (!isExcludedElement(element)) {
          var currentSize = window.getComputedStyle(element).fontSize;
          var newSize =  parseFloat(currentSize) + parseFloat(FontSizeStateBigger);
          element.style.setProperty('font-size', newSize + 'px', 'important');
  
  
          } 
        });
  
      }
  
          if (FontSizeStateSmaller != 0) {
            document.getElementById('btn-s9').disabled = true;
            var elements = document.querySelectorAll('*:not(.uw-widget-custom-trigger, .uw-widget-custom-trigger span)');
            elements.forEach(function(element) {
            // Exclude elements inside #uw-main and with class .uwaw-features__item__name
            if (!isExcludedElement(element)) {
            var currentSize = window.getComputedStyle(element).fontSize;
            var newSize =  parseFloat(currentSize) - parseFloat(FontSizeStateSmaller);
            element.style.setProperty('font-size', newSize + 'px', 'important');
  
    
          } 
        });
      }
        }
    
    });
  
  document.getElementById(btnId).addEventListener('click', function() {
  clickCount++;
  addsize += 2;
  var featureItem = document.getElementById(featureItemId);
  var featureSteps = document.getElementById(featureStepsId);
  var tickIcon = document.getElementById(tickIconId);
  
  if (btnId == "btn-s9") {document.getElementById('btn-small-text').disabled = true; localStorage.setItem('btn-big', true);}
  
  if (btnId == "btn-small-text") {document.getElementById('btn-s9').disabled = true; localStorage.setItem('btn-small', true);}
  
  // Save current state to local storage
  localStorage.setItem(Storageclick, clickCount);
  localStorage.setItem(ButtonStorageClick, true);
  
  
  // Reset on 5th click
  if (clickCount === 5) {
  clickCount = 0;
  addsize = 0;
  featureItem.classList.remove('feature-active');
  featureSteps.classList.remove('featureSteps-visible');
  featureSteps.innerHTML = '';
  tickIcon.style.display = 'none';
  localStorage.setItem(Storageclick, 0);
  localStorage.setItem(ButtonStorageClick, false);
  
  if (btnId == "btn-s9") {document.getElementById('btn-small-text').disabled = false; localStorage.setItem('btn-big', false);}
  if (btnId == "btn-small-text") {var otherBtn = document.getElementById('btn-s9').disabled = false; localStorage.setItem('btn-small', false);}
  
  // Reset font size of all elements
  resetFontSizes(btn, Storageclick, ButtonStorageClick);
  return;
  }
  // Add feature-active class on the first click
  if (clickCount === 1) {
      featureItem.classList.add('feature-active');
      featureSteps.classList.add('featureSteps-visible');
      localStorage.setItem(Storageclick, clickCount);
      localStorage.setItem(ButtonStorageClick, true);
  }
  
  // Update data-uw-reader-content attribute
  document.getElementById(btnId).setAttribute('data-uw-reader-content', clickCount);
  
  // Add step span tags dynamically
  var stepsHTML = '';
  for (var i = 0; i < 4; i++) {
    stepsHTML += '<span class="' + (i < clickCount ? 'active step uwaw-features__step' : 'step uwaw-features__step') + '"></span>';
  }
  featureSteps.innerHTML = stepsHTML;
  
  // Display tick icon until the 4th click
  if (clickCount < 5) {
   tickIcon.style.display = 'inline-block';
  }
  
  adjustFontSizes(increase, btn, addsize);
      });
  }
  
  function adjustFontSizes(increase, btn, addsize) {
  var SizeStorage = btn + '-size';
  var elements = document.querySelectorAll('*:not(.uw-widget-custom-trigger, .uw-widget-custom-trigger span)');
  elements.forEach(function(element) {
  // Exclude elements inside #uw-main and with class .uwaw-features__item__name
  if (!isExcludedElement(element)) {
  var currentSize = window.getComputedStyle(element).fontSize;
  var newSize = increase ? parseFloat(currentSize) + 2 : parseFloat(currentSize) - 2;
  // element.style.fontSize = newSize + 'px';
  element.style.setProperty('font-size', newSize + 'px', 'important');
  localStorage.setItem(SizeStorage, parseFloat(addsize));
          }
      });
  }
  
  // Reset font sizes
  function resetFontSizes() {
      var elements = document.querySelectorAll('*');
      elements.forEach(function(element) {
      // Reset font-size style for all elements
      element.style.fontSize = '';
      localStorage.setItem('st-size', 0);
      localStorage.setItem('st-clickCount', 0);
      localStorage.setItem('st-buttonClicked', false);
      localStorage.setItem('bt-size', 0);
      localStorage.setItem('bt-clickCount', 0);
      localStorage.setItem('bt-buttonClicked', false);
      localStorage.setItem('btn-big', false);
      localStorage.setItem('btn-small', false);
      });
  }
  
  
  // Usage
  handleFontSizes('btn-s9', 'featureItem', 'featureSteps', 'tickIcon', true, 'bt');  // For Bigger Text
  handleFontSizes('btn-small-text', 'featureItem-st', 'featureSteps-st', 'tickIcon-st', false, 'st');  // For Smaller Text
  
  // document.getElementById(btn-s9).addEventListener('click', function() { 
  
  
  
  // });
  
  // ******************************************************************************* //
  
  // text spacing 
  
  
  
  let letterSpacing = 0; // Initial letter spacing (auto)
  let clickCountText = 0; // Counter to track button clicks
  
  // Check local storage for previous state
  var localStorageSpacingCount = localStorage.getItem('ts-clickCount');
  if (localStorageSpacingCount) {
    clickCountText = parseInt(localStorageSpacingCount, 10);
  }
  
  
  function increaseAndReset() {
    clickCountText++;
  var featureItem_ts = document.getElementById('featureItem-ts');
  var featureSteps_ts = document.getElementById('featureSteps-ts');
  var tickIcon_ts = document.getElementById('tickIcon-ts');
  
  // Save current state to local storage
  localStorage.setItem('ts-clickCount', clickCountText);
  localStorage.setItem('ts-buttonClicked',true);
    
  // Reset letter spacing after the third click
  if (clickCountText === 4) {
  letterSpacing = 0; // Reset letter spacing to auto (0)
  clickCountText = 0; // Reset click count
  featureItem_ts.classList.remove('feature-active');
  featureSteps_ts.classList.remove('featureSteps-visible');
  featureSteps_ts.innerHTML = '';
  tickIcon_ts.style.display = 'none';
  
  // Save current state to local storage
  localStorage.setItem('ts-clickCount', clickCountText);
  localStorage.setItem('ts-buttonClicked',false);
  
  // Reset font size of all elements
  resetLetterspacing();
  return;
  }
  
  // Add feature-active class on the first click
  if (clickCountText === 1) {
    featureItem_ts.classList.add('feature-active');
    featureSteps_ts.classList.add('featureSteps-visible');
  
    // Save current state to local storage
    localStorage.setItem('ts-clickCount', clickCountText);
    localStorage.setItem('ts-buttonClicked',true);
    }
              
  // Add step span tags dynamically
  var stepsHTML_ts = '';
    for (var i = 0; i < 3; i++) {
    stepsHTML_ts += '<span class="' + (i < clickCountText ? 'active step uwaw-features__step' : 'step uwaw-features__step') + '"></span>';
    }
    featureSteps_ts.innerHTML = stepsHTML_ts;
  // Display tick icon until the 4th click
  if (clickCountText < 4) {
    tickIcon_ts.style.display = 'inline-block';
  }
  
  letterSpacing += 2; // Increase by 5px
    applyLetterSpacing();
  }
  
  function decreaseSpacing() {
    letterSpacing -= 5; // Decrease by 5px
    applyLetterSpacing();
    }
  
  function applyLetterSpacing() {
  const elements = document.querySelectorAll('*:not(.uw-widget-custom-trigger, .uw-widget-custom-trigger span)'); // Select all elements except buttons
    elements.forEach(function(element) {
    if (!isExcludedElement(element)) {
  
          var currentSize_ts = parseFloat(window.getComputedStyle(element).letterSpacing);
          currentSize_ts = isNaN(currentSize_ts) ? 0 : currentSize_ts; // Handle cases where lineHeight is 'normal' or an invalid value
  
          // Convert to pixels (optional, depending on your needs)
          currentSize_ts = currentSize_ts + 'px';
          var newSize_ts = parseFloat(currentSize_ts) + 2;
          // element.style.letterSpacing = newSize_ts;
          element.style.setProperty('letter-spacing', newSize_ts + 'px', 'important');
          localStorage.setItem('ts-spacing', parseFloat(newSize_ts));
          }
        });
      }
  
  function resetLetterspacing() {
  var elements = document.querySelectorAll('*:not(.uw-widget-custom-trigger, .uw-widget-custom-trigger span)');
  elements.forEach(function (element) {
  // Reset font-size style for all elements
  element.style.letterSpacing = ''; // Reset to default or "normal"
  localStorage.setItem('ts-spacing', null);
  localStorage.setItem('ts-clickCount', 0);
  localStorage.setItem('ts-buttonClicked', false);
  });
  }
  
  // Check and restore the state from localStorage on page load
  document.addEventListener('DOMContentLoaded', function() { 
  
    var featureItem_ts = document.getElementById('featureItem-ts');
  var featureSteps_ts = document.getElementById('featureSteps-ts');
  var tickIcon_ts = document.getElementById('tickIcon-ts');
    
    // Restore tickIcon visibility
    var SpacingState = JSON.parse(localStorage.getItem('ts-buttonClicked'));
    var SpacingClickState = JSON.parse(localStorage.getItem('ts-clickCount'));
    var SpacingSizeState = localStorage.getItem('ts-spacing');
  
    console.log( SpacingSizeState);
    
    if (SpacingState) {
    
      tickIcon_ts.style.display = 'inline-block';
      featureItem_ts.classList.add('feature-active');
      featureSteps_ts.classList.add('featureSteps-visible');
    
      var stepsHTML_ts = '';
      for (var i = 0; i < 3; i++) {
          stepsHTML_ts += '<span class="' + (i < SpacingClickState ? 'active step uwaw-features__step' : 'step uwaw-features__step') + '"></span>';
      }
      featureSteps_ts.innerHTML = stepsHTML_ts;
    
      const elements = document.querySelectorAll('*:not(.uw-widget-custom-trigger, .uw-widget-custom-trigger span)'); // Select all elements except buttons
    elements.forEach(function(element) {
    if (!isExcludedElement(element)) {
  // Handle cases where lineHeight is 'normal' or an invalid value
  
      // Convert to pixels (optional, depending on your needs)
      // currentSize_ts = SpacingSizeState + 'px';
      // element.style.letterSpacing = SpacingSizeState + 'px';
      element.style.setProperty('letter-spacing', SpacingSizeState + 'px', 'important');
          }
        });
    }
    
    });
  
  
  // ******************************************************************************* //
  
  // Line height script
  
  var clickCount_lh = 0;
  
  // Check local storage for previous state
  var localStorageClickCount = localStorage.getItem('lh-clickCount');
  if (localStorageClickCount) {
    clickCount_lh = parseInt(localStorageClickCount, 10);
  }
  
  document.getElementById('btn-s12').addEventListener('click', function() {
  clickCount_lh++;
  var featureItem_lh = document.getElementById('featureItem-lh');
  var featureSteps_lh = document.getElementById('featureSteps-lh');
  var tickIcon_lh = document.getElementById('tickIcon-lh');
  
    // Save current state to local storage
    localStorage.setItem('lh-clickCount', clickCount_lh);
    localStorage.setItem('lh-buttonClicked', true);
  
  // Reset on 5th click
  if (clickCount_lh === 4) {
    clickCount_lh = 0;
    featureItem_lh.classList.remove('feature-active');
    featureSteps_lh.classList.remove('featureSteps-visible');
    featureSteps_lh.innerHTML = '';
    tickIcon_lh.style.display = 'none';
    // Reset font size of all elements
  
    // Save current state to local storage
    localStorage.setItem('lh-clickCount', 0);
    localStorage.setItem('lh-buttonClicked', false);
  
    resetlineheight();
    return;
  }
  
  // Add feature-active class on the first click
  if (clickCount_lh === 1) {
      featureItem_lh.classList.add('feature-active');
      featureSteps_lh.classList.add('featureSteps-visible');
      localStorage.setItem('lh-clickCount', 1);
    localStorage.setItem('lh-buttonClicked', true);
  }
  
  // Update data-uw-reader-content attribute
  document.getElementById('btn-s12').setAttribute('data-uw-reader-content', clickCount_lh);
  // Add step span tags dynamically
  var stepsHTML_lh = '';
  for (var i = 0; i < 3; i++) {
      stepsHTML_lh += '<span class="' + (i < clickCount_lh ? 'active step uwaw-features__step' : 'step uwaw-features__step') + '"></span>';
  }
  featureSteps_lh.innerHTML = stepsHTML_lh;
  // Display tick icon until the 4th click
  if (clickCount_lh < 4) {
      tickIcon_lh.style.display = 'inline-block';
  }
  
  increaseLineheight();
  
  });
  
  function increaseLineheight() {
  var elements = document.querySelectorAll('*:not(.uw-widget-custom-trigger, .uw-widget-custom-trigger span)');
    elements.forEach(function(element) {
       // Exclude elements inside #uw-main and with class .uwaw-features__item__name
       if (!isExcludedElement(element)) {
          var currentSize_lh = parseFloat(window.getComputedStyle(element).lineHeight);
          currentSize_lh = isNaN(currentSize_lh) ? 0 : currentSize_lh; // Handle cases where lineHeight is 'normal' or an invalid value
  
    // Convert to pixels (optional, depending on your needs)
    currentSize_lh = currentSize_lh + 'px';
    var newSize_lh = parseFloat(currentSize_lh) + 10 + 'px';
    localStorage.setItem('lh-height', parseFloat(newSize_lh));
    // element.style.lineHeight = newSize_lh;
    element.style.setProperty('line-height', newSize_lh, 'important'); /*add er*/
  
       }
   });
  }
  
  function resetlineheight() {
  var elements = document.querySelectorAll('*');
  elements.forEach(function (element) {
  // Reset font-size style for all elements
  element.style.lineHeight = ''; // Reset to default or "normal"
  localStorage.setItem('lh-height', null);
  localStorage.setItem('lh-clickCount', 0);
  localStorage.setItem('lh-buttonClicked', false);
  });
  }
  
  // Check and restore the state from localStorage on page load
  document.addEventListener('DOMContentLoaded', function() { 
  
  var featureItem_lh = document.getElementById('featureItem-lh');
  var featureSteps_lh = document.getElementById('featureSteps-lh');
  var tickIcon_lh = document.getElementById('tickIcon-lh');
  
  // Restore tickIcon visibility
  var LineHeightState = JSON.parse(localStorage.getItem('lh-buttonClicked'));
  var LineHeightClickState = JSON.parse(localStorage.getItem('lh-clickCount'));
  var LineHeightSizeState = localStorage.getItem('lh-height');
  
  if (LineHeightState) {
  
    tickIcon_lh.style.display = 'inline-block';
    featureItem_lh.classList.add('feature-active');
    featureSteps_lh.classList.add('featureSteps-visible');
  
    var stepsHTML_lh = '';
    for (var i = 0; i < 3; i++) {
        stepsHTML_lh += '<span class="' + (i < LineHeightClickState ? 'active step uwaw-features__step' : 'step uwaw-features__step') + '"></span>';
    }
    featureSteps_lh.innerHTML = stepsHTML_lh;
  
    var elements = document.querySelectorAll('*');
    elements.forEach(function(element) {
       // Exclude elements inside #uw-main and with class .uwaw-features__item__name
       if (!isExcludedElement(element)) {
          var currentSize_lh = parseFloat(window.getComputedStyle(element).lineHeight);
          currentSize_lh = isNaN(currentSize_lh) ? 0 : currentSize_lh; // Handle cases where lineHeight is 'normal' or an invalid value
  
        // Convert to pixels (optional, depending on your needs)
        currentSize_lh = currentSize_lh + 'px';
        var newSize_lh = parseFloat(currentSize_lh) + parseFloat(LineHeightSizeState) + 'px';
        element.style.setProperty('line-height', newSize_lh, 'important');
       }
     });
  
  }
  
  });
  
  /***********************************************************************************************************/
  
  // Hide Images Script
  
  // Function to toggle the visibility of images
  function toggleImages() {
    document.documentElement.classList.toggle('image-hide');
    document.documentElement.id = document.documentElement.classList.contains('image-hide') ? 'imageHideBg' : '';
    var images = document.querySelectorAll('img');
    // var bgRemove = document.querySelectorAll('*');
    var imageVisibilityState = {};
    // var bgimageVisibilityState = {};
    var tickIcon_ht = document.getElementById('tickIcon-hi');
    var featureItem = document.getElementById('featureItem-hi');
  
    // Toggle the visibility of images
    images.forEach(function (image, index) {
        if (!isExcludedElement(image)) {
          image.style.setProperty('visibility', image.style.visibility === 'hidden' ? 'visible' : 'hidden', 'important');
          imageVisibilityState[index] = image.style.visibility;
          
        }
    });
  
  
    // Toggle the visibility of the tickIcon
    tickIcon_ht.style.display = tickIcon_ht.style.display === 'none' ? 'inline-block' : 'none';
  
    // Toggle the feature-active class on featureItem
    featureItem.classList.toggle('feature-active');
  
    localStorage.setItem('imageVisibilityState', JSON.stringify(imageVisibilityState));
  
  }
  
  // Check and restore the state from localStorage on page load
  document.addEventListener('DOMContentLoaded', function() {
  
    var tickIcon_ht = document.getElementById('tickIcon-hi');
    var featureItem = document.getElementById('featureItem-hi');
    var images = document.querySelectorAll('img');
  
    // Restore tickIcon visibility
    var imageVisibilityState = JSON.parse(localStorage.getItem('imageVisibilityState'));
  
    if (imageVisibilityState) {
      images.forEach(function (image, index) {
          if (!isExcludedElement(image) && imageVisibilityState[index]) {
            image.style.setProperty('visibility', imageVisibilityState[index], 'important');
  
          }
      });
    }
  
    if (imageVisibilityState && imageVisibilityState['1'] === 'hidden') {
        tickIcon_ht.style.display = 'inline-block';
        featureItem.classList.add('feature-active');
        document.documentElement.classList.toggle('image-hide');
        document.documentElement.id = document.documentElement.classList.contains('image-hide') ? 'imageHideBg' : '';
    }
  });
  
  // ******************************************************************************************************//
  
  // light dark mode
  
  // Toggle dark mode and save additional state when the button with ID 'dark-btn' is clicked
  document.getElementById('dark-btn').addEventListener('click', function() {
  
      var tickIcon_ht_dark = document.getElementById('tickIcon-ht-dark');
      var featureItemDrak = document.getElementById('featureItem-ht-dark');
      const checkbox = document.getElementById("checkbox");
  
      const isDarkMode = checkbox.checked;
      document.body.classList.toggle("dark", isDarkMode);
  
      // Toggle the visibility of the tickIcon
      tickIcon_ht_dark.style.display = tickIcon_ht_dark.style.display === 'none' ? 'inline-block' : 'none';
  
      // Toggle the feature-active class on featureItem
      featureItemDrak.classList.toggle('feature-active');
  
      // Save the state to local storage
      localStorage.setItem("darkMode", isDarkMode);
  
  });
  
  // Call applyDarkModeOnLoad function on page load
  document.addEventListener('DOMContentLoaded', function() {
  
    var tickIcon_ht_dark = document.getElementById('tickIcon-ht-dark');
    var featureItemDrak = document.getElementById('featureItem-ht-dark');
    const checkbox = document.getElementById("checkbox");
  
    const isDarkMode = JSON.parse(localStorage.getItem('darkMode'));
    if (isDarkMode === true) {
    checkbox.checked = isDarkMode;
    document.body.classList.add("dark");
    tickIcon_ht_dark.style.display = 'inline-block';
    featureItemDrak.classList.toggle('feature-active');
    }
  
  });
  
  /******************************************************************************************************/
  
  //Highlight Links Script
  
  // Function to toggle the highlight links feature and save state in local storage
  function highlightLinks() {
  
    var tickIcon_ht = document.getElementById('tickIcon-ht');
    var featureItem = document.getElementById('featureItem-ht');
    var HighlightLinkState = [];
  
    // Toggle the visibility of the tickIcon
    tickIcon_ht.style.display = tickIcon_ht.style.display === 'none' ? 'inline-block' : 'none';
  
    // Toggle the feature-active class on featureItem
    featureItem.classList.toggle('feature-active');
  
    // Toggle the highlight of links
    var links = document.querySelectorAll('a');
    links.forEach(function (link, index) {
        if (!isExcludedElement(link)) {
            link.style.setProperty('background', link.style.background ? '' : 'black', 'important');
            link.style.setProperty('color', link.style.color ? '' : 'yellow', 'important');
            // Set HighlightLinkState based on the background color
            HighlightLinkState = link.style.getPropertyValue('background') === 'black !important' && link.style.getPropertyValue('color') === 'yellow !important';
        }
    });
  
    // Save state in local storage
    localStorage.setItem("highlightLinks", JSON.stringify(HighlightLinkState));
  }
  
  // Check and restore the state from localStorage on page load
  document.addEventListener('DOMContentLoaded', function() {
  
    var tickIcon_ht = document.getElementById('tickIcon-ht');
    var featureItem = document.getElementById('featureItem-ht');
    var links = document.querySelectorAll('a');
  
    // Restore tickIcon visibility
    var GetHighlightLinkState = JSON.parse(localStorage.getItem('highlightLinks'));
    if (GetHighlightLinkState === true) {
      links.forEach(function (link, index) {
          if (!isExcludedElement(link) && GetHighlightLinkState) {
            link.style.setProperty('background', link.style.background ? '' : '#1C1D1F', 'important');
            link.style.setProperty('color', link.style.color ? '' : 'yellow', 'important');
          }
      });
    }
  
    if (GetHighlightLinkState && GetHighlightLinkState === true) {
        tickIcon_ht.style.display = 'inline-block';
        featureItem.classList.add('feature-active');
    }
  });
  
  /*******************************************************************************************************/
  
  //Cursor Script
  
  // Function to toggle the cursor feature and save state in local storage
  function toggleCursorFeature() {
    // Toggle the 'ux4g-bg-cursor' class on the body
    document.documentElement.classList.toggle('ux4g-bg-cursor');
  
    // Toggle the tick icon
    var tickIcon_cursor = document.getElementById('tickIcon-cursor');
    tickIcon_cursor.style.display = tickIcon_cursor.style.display === 'none' ? 'inline-block' : 'none';
  
    var featureItem = document.getElementById('featureItem-Cursor');
  
    // Toggle the feature-active class on featureItem
    featureItem.classList.toggle('feature-active');
  
    // Save state in local storage
    localStorage.setItem("cursorFeatureActive", featureItem.classList.contains('feature-active'));
  }
  
  document.addEventListener('DOMContentLoaded', function() { 
  
    var GetCursorState = JSON.parse(localStorage.getItem('cursorFeatureActive'));
    var tickIcon_cursor = document.getElementById('tickIcon-cursor');
    var featureItem = document.getElementById('featureItem-Cursor');
  
    if (GetCursorState === true) { 
      document.documentElement.classList.add('ux4g-bg-cursor');
      tickIcon_cursor.style.display = 'inline-block';
      featureItem.classList.add('feature-active');
    }
  
  });
  
  
  /*****************************************************************************************************/
  
  //Dyslexia Font Code
  
  function toggleFontFeature() {
  
    // Toggle the 'ux4g-font-df' class on the body
    document.documentElement.classList.toggle('ux4g-font-df');
  
    // Toggle the tick icon
    var tickIcon_df = document.getElementById('tickIcon-df');
    tickIcon_df.style.display = tickIcon_df.style.display === 'none' ? 'inline-block' : 'none';
  
    var featureItem = document.getElementById('featureItem-df');
  
    // Toggle the feature-active class on featureItem
    featureItem.classList.toggle('feature-active');
  
    // Save state in local storage
    localStorage.setItem("dyslexia", document.documentElement.classList.contains('ux4g-font-df'));
  
  }
  
  document.addEventListener('DOMContentLoaded', function() { 
  
    var GetdyslexiaState = JSON.parse(localStorage.getItem('dyslexia'));
    var tickIcon_df = document.getElementById('tickIcon-df');
    var featureItem_df = document.getElementById('featureItem-df');
  
    if (GetdyslexiaState === true) { 
      document.documentElement.classList.add('ux4g-font-df');
      tickIcon_df.style.display = 'inline-block';
      featureItem_df.classList.add('feature-active');
    }
  
  });
  
  /***************************************************************************************************/
  
  // invert script
  
  // Function to toggle the 'Invert' feature
  document.getElementById('btn-invert').addEventListener('click', function() {
  
    // Toggle the 'invert' class on the body
    document.documentElement.classList.toggle('ux4g-bg-white');
  
    // Toggle the tick icon
    var tickIcon_ic = document.getElementById('tickIcon-ic');
    tickIcon_ic.style.display = tickIcon_ic.style.display === 'none' ? 'inline-block' : 'none';
  
    var featureItem = document.getElementById('featureItem-ic');
  
    // Toggle the feature-active class on featureItem
    featureItem.classList.toggle('feature-active');
  
    // Save the state in localStorage
    localStorage.setItem('invertFeature', document.documentElement.classList.contains('ux4g-bg-white'));
  
  });
  
  document.addEventListener('DOMContentLoaded', function() { 
  
    var GetInvertState = JSON.parse(localStorage.getItem('invertFeature'));
    var tickIcon_ic = document.getElementById('tickIcon-ic');
    var featureItem_ic = document.getElementById('featureItem-ic');
  
    if (GetInvertState === true) { 
      document.documentElement.classList.add('ux4g-bg-white');
      tickIcon_ic.style.display = 'inline-block';
      featureItem_ic.classList.add('feature-active');
    }
  
  });
  
  /***************************************************************************************************/
  
  // Show Hide Main Widgets Div on Click
  document.getElementById('uw-widget-custom-trigger').addEventListener('click', function() {
      openMain();
  });
  // document.getElementById('uw-widget-custom-trigger2').addEventListener('click', function() {
  //   openMain();
  // });
  function openMain() {
      var mainElement = document.getElementById('uw-main');    
      mainElement.style.right = '0px';    
  }
  function closeMain() {
      var mainElement = document.getElementById('uw-main');   
      mainElement.style.right = '-490px';
  
  }
  
  /***************************************************************************************************/
  
  // Reset All Script
  
  function resetAll() {
  
      var resetFeatures = document.querySelectorAll('.reset-feature');
    resetFeatures.forEach(function (feature) {
      feature.classList.remove('feature-active');
    });
  
    // Hide spans with class 'reset-tick'
    var resetTicks = document.querySelectorAll('.reset-tick');
    resetTicks.forEach(function (tick) {
      tick.style.display = 'none';
    });
  
    // Remove yellow highlight color on links
    var links = document.querySelectorAll('a');
    links.forEach(function (link) {
      link.style.background = '';
      link.style.color = '';
    });
  
    localStorage.setItem('highlightLinks', false);
  
    // Make Images Visible
  
      var images = document.querySelectorAll('img');
      images.forEach(function (image) {
          image.style.visibility = 'visible';
      });
  
      var resetImageVisibilityState = {};
      localStorage.setItem('imageVisibilityState', JSON.stringify(resetImageVisibilityState));
  
      document.documentElement.classList.remove('image-hide');
      document.documentElement.id = document.documentElement.classList.contains('image-hide') ? 'imageHideBg' : '';
  
  
      //Make Invert to default
  
      document.documentElement.classList.remove('ux4g-bg-white');
      localStorage.setItem('invertFeature', false);
  
      // Make font to default
  
      document.documentElement.classList.remove('ux4g-font-df');
      localStorage.setItem("dyslexia", false);
  
      // Make cursor default
  
      document.documentElement.classList.remove('ux4g-bg-cursor');
      localStorage.setItem("cursorFeatureActive", false);
  
      // Make Light-Dark to default
  
      // Uncheck
     var reset_check = document.getElementById("checkbox").checked = false;
     document.body.classList.remove("dark", reset_check);
     localStorage.setItem("darkMode", false);
  
      //Reset Lineheight
    
      resetlineheight();
      
  
      // Reset Ltter Spacing
      resetLetterspacing();
  
      //Reset Font Sizes
      resetFontSizes();
      document.getElementById('btn-s9').disabled = false;
      document.getElementById('btn-small-text').disabled = false;
      
      // Remove inner HTML of parent divs with class 'reset-steps'
      var resetSteps = document.querySelectorAll('.reset-steps');
      resetSteps.forEach(function (step) {
          step.innerHTML = '';
          step.classList.remove('featureSteps-visible');
      });
  
      //Reset Speech
      resetspeech();
      localStorage.setItem("speak", false);
  
    }
  
  
    /*****************  Screen Reader Script*************/  
  
    document.getElementById('speak').addEventListener('click', function() {
      // Toggle the tick icon
      var tickIcon_sp = document.getElementById('tickIcon_sp');
      tickIcon_sp.style.display = tickIcon_sp.style.display === 'none' ? 'inline-block' : 'none';
    
      var featureItem_sp = document.getElementById('featureItem_sp');
    
      // Toggle the feature-active class on featureItem
      featureItem_sp.classList.toggle('feature-active'); 
  
      // Save state in local storage
      localStorage.setItem("speak", featureItem_sp.classList.contains('feature-active'));
      
      
    });
  
  
  
  // grab the UI elements to work with
  const speakEl = document.getElementById('speak');
  let isReading = false;
  let utterance = null;
  let previousSelectedElement = null; 
  
  // Create audio elements for sound effects
  const speakOnSound = new Audio(''); 
  const speakOffSound = new Audio(''); 
  
  document.addEventListener('mouseup', function (event) {
    if (isReading) {
      const clickedElement = event.target;
  
      // Check if the clicked element can contain text content
      const allowedTags = ['P', 'SPAN', 'DIV', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'A', 'LI', 'LABEL', 'BUTTON', 'TD', 'TH', 'STRONG', 'EM', 'B', 'I', 'U', 'SMALL', 'BIG', 'SUB', 'SUP'];
  
      if (allowedTags.includes(clickedElement.tagName.toUpperCase())) {
        selectAndSpeak(clickedElement);
      }
    }
  });
  
  // click handler for the "Speak On" button
  speakEl.addEventListener('click', toggleSpeech);
  
  function toggleSpeech() {
    if (!isReading) {
      // Enable speech
      speakOnSound.play(); 
      isReading = true;
    } else {
      // Disable speech
      resetspeech();
    }
  }
  
  function resetspeech() {
    speakOffSound.play(); 
    window.speechSynthesis.cancel();
    isReading = false;
    previousSelectedElement = null; 
  }
  
  function startReading(text) {
    utterance = new SpeechSynthesisUtterance(text);
  
    // Set properties for a more formal voice
    utterance.rate = 0.7; // Adjust the rate (0.5 is slower, 2.0 is faster)
    utterance.pitch = 10.0; // Set pitch to 1.0 for a natural voice
  
    // Attempt to set a female voice
    const voices = window.speechSynthesis.getVoices();
    const femaleVoice = voices.find(voice => voice.name.includes('female') && voice.lang.includes('en'));
    if (femaleVoice) {
      utterance.voice = femaleVoice;
    }
  
    window.speechSynthesis.speak(utterance);
  
    // Add an event listener for the 'end' event to reset the selection
    utterance.addEventListener('end', function () {
      resetSelection();
    });
  }
  
  function selectAndSpeak(element) {
    const range = document.createRange();
    range.selectNodeContents(element);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  
    if (previousSelectedElement !== element) {
      // If a different element is clicked, cancel the current speech
      window.speechSynthesis.cancel();
      startReading(selection.toString());
      previousSelectedElement = element; 
    } else {
      // If the same element is clicked, toggle between play/pause
      if (isReading) {
        window.speechSynthesis.pause();
      } else {
        window.speechSynthesis.resume();
      }
    }
  }
  
  function resetSelection() {
    const selection = window.getSelection();
    selection.removeAllRanges();
    previousSelectedElement = null;
  }
  
  document.addEventListener('DOMContentLoaded', function() { 
    var GetspeakState = JSON.parse(localStorage.getItem('speak'));
    var tickIcon_sp = document.getElementById('tickIcon_sp');
    var featureItem_sp = document.getElementById('featureItem_sp');
  
    if (GetspeakState === true) { 
      tickIcon_sp.style.display = 'inline-block';
      featureItem_sp.classList.add('feature-active');
      speakOnSound.play(); 
      isReading = true;
    }
  });
  
  
  
    
  
  // end here
  
  
  