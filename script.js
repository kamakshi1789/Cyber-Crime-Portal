// ======================================
// CYBER SECURE PORTAL JAVASCRIPT
// ======================================

console.log("Cyber Secure Portal Loaded");


// ======================================
// TABLE SEARCH FUNCTION
// ======================================

const searchInput = document.getElementById("searchInput");

if(searchInput){

    searchInput.addEventListener("keyup", function(){

        let filter =
        searchInput.value.toLowerCase();

        let rows =
        document.querySelectorAll("table tr");

        rows.forEach((row,index)=>{

            // SKIP HEADER

            if(index === 0) return;

            let text =
            row.innerText.toLowerCase();

            row.style.display =
            text.includes(filter)
            ? ""
            : "none";

        });

    });

}


// ======================================
// SIMPLE FORM VALIDATION
// ======================================

const forms =
document.querySelectorAll("form");

forms.forEach(form => {

    form.addEventListener("submit", function(e){

        const inputs =
        form.querySelectorAll("input[required], textarea[required], select[required]");

        let valid = true;

        inputs.forEach(input => {

            if(input.value.trim() === ""){

                valid = false;

                input.style.border =
                "1px solid red";

            }
            else{

                input.style.border =
                "1px solid #cbd5e1";

            }

        });

        if(!valid){

            e.preventDefault();

            alert(
                "Please fill all required fields."
            );

        }

    });

});


// ======================================
// ALERT MESSAGE AUTO HIDE
// ======================================

setTimeout(()=>{

    const errorMessages =
    document.querySelectorAll(".error-message");

    errorMessages.forEach(msg=>{

        msg.style.display = "none";

    });

},4000);


// ======================================
// SIDEBAR NAVIGATION ACTIVE HIGHLIGHT
// ======================================

document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".sidebar ul li a");

    navLinks.forEach(link => {
        const href = link.getAttribute("href");
        // Check if the current pathname matches the link's href
        if (href === currentPath || (currentPath === "/" && href === "/")) {
            link.classList.add("active");
        } else if (currentPath !== "/" && href !== "/" && currentPath.startsWith(href)) {
            // Also handle sub-paths
            link.classList.add("active");
        }
    });

    // Awareness guidelines toggle
    const toggleButtons = document.querySelectorAll(".toggle-guidelines-btn");
    toggleButtons.forEach(button => {
        button.addEventListener("click", () => {
            const card = button.closest(".awareness-card");
            if (!card) return;

            const box = card.querySelector(".precautions-box");
            if (!box) return;

            const isOpen = box.classList.contains("open");
            if (isOpen) {
                box.classList.remove("open");
                button.innerHTML = 'View Guidelines <i class="fa-solid fa-chevron-down"></i>';
            } else {
                box.classList.add("open");
                button.innerHTML = 'Hide Guidelines <i class="fa-solid fa-chevron-up"></i>';
            }
        });
    });

    // Auto-scroll chat boxes to bottom on load
    const chatBoxes = document.querySelectorAll(".chat-messages-box");
    chatBoxes.forEach(box => {
        box.scrollTop = box.scrollHeight;
    });
});

// ======================================
// COMPLAINT DETAILS EXPAND / COLLAPSE
// ======================================

function toggleDetails(id) {
    const detailsRow = document.getElementById(id);
    if (detailsRow) {
        const isHidden = detailsRow.style.display === "none" || detailsRow.style.display === "";
        detailsRow.style.display = isHidden ? "table-row" : "none";
        
        // Auto scroll chat box inside expanded details row if present
        if (isHidden) {
            setTimeout(() => {
                const box = detailsRow.querySelector(".chat-messages-box");
                if (box) box.scrollTop = box.scrollHeight;
            }, 50);
        }
    }
}

// ======================================
// USER COMPLAINT CARD EXPAND / COLLAPSE
// ======================================

function toggleTrackCard(id) {
    const bodyEl = document.getElementById("expandable-" + id);
    const btnEl = document.getElementById("toggle-btn-" + id);
    if (bodyEl) {
        const isHidden = bodyEl.style.display === "none" || bodyEl.style.display === "";
        bodyEl.style.display = isHidden ? "block" : "none";
        
        // Update button arrow and text
        if (btnEl) {
            btnEl.innerHTML = isHidden 
                ? 'Collapse Case <i class="fa-solid fa-chevron-up"></i>' 
                : 'Expand Case <i class="fa-solid fa-chevron-down"></i>';
        }
        
        // Auto scroll chat box if opened
        if (isHidden) {
            setTimeout(() => {
                const box = bodyEl.querySelector(".chat-messages-box");
                if (box) box.scrollTop = box.scrollHeight;
            }, 50);
        }
    }
}


// ======================================
// INTEGRATED PORTAL VALIDATION & CONSENT
// ======================================

document.addEventListener("DOMContentLoaded", () => {
    const declareConsent = document.getElementById("declareConsent");
    const submitBtn = document.getElementById("submitComplaintBtn");
    const evidenceInput = document.getElementById("evidenceInput");
    const evidenceError = document.getElementById("evidenceError");

    // Manage Consent Checkbox
    if (declareConsent && submitBtn) {
        // Init state on page load
        submitBtn.disabled = !declareConsent.checked;

        declareConsent.addEventListener("change", () => {
            submitBtn.disabled = !declareConsent.checked;
        });
    }

    // Client-side file validation (Allowed formats: PNG, JPG, JPEG, PDF, MP4; Max size: 5MB)
    if (evidenceInput && evidenceError) {
        evidenceInput.addEventListener("change", function () {
            const file = this.files[0];
            if (!file) {
                evidenceError.style.display = "none";
                evidenceInput.style.border = "1px solid #cbd5e1";
                return;
            }

            // Check file size (5MB = 5 * 1024 * 1024 bytes)
            const maxSize = 5 * 1024 * 1024;
            const allowedExtensions = ["png", "jpg", "jpeg", "pdf", "mp4"];
            const fileName = file.name.toLowerCase();
            const fileExtension = fileName.split('.').pop();

            let isExtensionValid = allowedExtensions.includes(fileExtension);
            let isSizeValid = file.size <= maxSize;

            if (!isExtensionValid) {
                evidenceError.textContent = "❌ Invalid format. Only PNG, JPG, JPEG, PDF, and MP4 files are allowed.";
                evidenceError.style.display = "block";
                evidenceInput.style.border = "1.5px solid #dc2626";
                this.value = ""; // Reset file selection
                return;
            }

            if (!isSizeValid) {
                evidenceError.textContent = "❌ File is too large. Maximum allowed size is 5MB.";
                evidenceError.style.display = "block";
                evidenceInput.style.border = "1.5px solid #dc2626";
                this.value = ""; // Reset file selection
                return;
            }

            // If everything is valid
            evidenceError.style.display = "none";
            evidenceInput.style.border = "1.5px solid #10b981"; // Green validation highlight
        });
    }

    // Form reset handler
    const complaintForm = document.getElementById("complaintForm");
    if (complaintForm) {
        complaintForm.addEventListener("reset", () => {
            setTimeout(() => {
                if (submitBtn) {
                    submitBtn.disabled = true;
                }
                if (evidenceError) {
                    evidenceError.style.display = "none";
                }
                if (evidenceInput) {
                    evidenceInput.style.border = "1px solid #cbd5e1";
                }
            }, 0);
        });
    }
});

// CATEGORY FILTER SYSTEM

const filterButtons =
document.querySelectorAll(".filter-btn");

const complaintRows =
document.querySelectorAll(".complaint-row");

filterButtons.forEach(button => {

    button.addEventListener("click", () => {

        filterButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        const category =
        button.dataset.category;

        complaintRows.forEach(row => {

            const rowCategory =
            row.dataset.category;

            if (
                category === "all" ||
                rowCategory === category
            ) {

                row.style.display = "";

            }

            else {

                row.style.display = "none";

            }

        });

    });

});