export function renderGoogleButton(containerId, clientId, onSuccess) {
  if (!clientId || !clientId.includes('.apps.googleusercontent.com')) {
    console.error("Invalid Google client ID:", clientId);
    return;
  }
  // Wait for GIS to load
  const ready = () =>
    typeof google !== "undefined" && google.accounts && google.accounts.id;

  const init = () => {
    if (!ready()) return setTimeout(init, 50);

    google.accounts.id.initialize({
      client_id: clientId,
      callback: onSuccess,        // receives { credential }
      ux_mode: "popup",
      auto_select: false
    });

    const el = document.getElementById(containerId);
    if (!el) return console.error("Container not found:", containerId);

    // Render official GIS button that opens the account chooser popup
    google.accounts.id.renderButton(el, {
      theme: "outline",
      size: "large",
      text: "signin_with",
      shape: "rectangular"
    });
  };

  init();
}



// export function startGoogleFlow(buttonId, clientId, onSuccess) {
//     console.log("Starting Google flow with client ID:", clientId);
    
//     // Validate client ID format
//     if (!clientId || !clientId.includes('.apps.googleusercontent.com')) {
//       console.error("Invalid Google client ID format:", clientId);
//       return;
//     }
    
//     // Check if Google Identity Services is loaded
//     if (typeof google === 'undefined' || !google.accounts || !google.accounts.id) {
//       console.error("Google Identity Services not loaded");
//       return;
//     }
    
//     // Initialize Google Identity Services
//     try {
//       google.accounts.id.initialize({
//         client_id: clientId,
//         callback: onSuccess,
//         ux_mode: "popup",
//         auto_select: false,
//         cancel_on_tap_outside: true,
//       });
//       console.log("Google Identity initialized successfully");
//     } catch (error) {
//       console.error("Error initializing Google Identity:", error);
//       return;
//     }
    
//     // Set up button click handler
//     document.getElementById(buttonId).onclick = () => {
//       console.log("Google button clicked");
//       try {
//         google.accounts.id.prompt((notification) => {
//           console.log("Google prompt notification:", notification);
//           if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
//             console.error("Google prompt not displayed or skipped:", notification.getNotDisplayedReason());
//             console.error("Not displayed reason:", notification.getNotDisplayedReason());
//             console.error("Skipped moment reason:", notification.getSkippedMomentReason());
            
//             // Provide specific guidance based on the error
//             const reason = notification.getNotDisplayedReason() || notification.getSkippedMomentReason();
//             if (reason === 'popup_closed_by_user') {
//               console.error("User closed the popup");
//             } else if (reason === 'popup_blocked') {
//               console.error("Popup was blocked by browser - try disabling popup blockers");
//             } else if (reason === 'invalid_client') {
//               console.error("Invalid client ID - check Google Cloud Console configuration");
//             } else if (reason === 'unauthorized_client') {
//               console.error("Unauthorized client - check authorized origins in Google Cloud Console");
//             } else if (reason === 'network_error') {
//               console.error("Network error - check internet connection and CORS settings");
//             } else if (reason === 'access_denied') {
//               console.error("Access denied - check Google OAuth client configuration");
//             } else {
//               console.error("Unknown reason:", reason);
//             }
//           }
//         });
//       } catch (error) {
//         console.error("Error prompting Google Identity:", error);
//       }
//     };
//   }
