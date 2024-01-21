function iconCamera() {
    return `
        <svg class="object-contain w-full h-full" xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="83.253" height="72.684" fill-rule="evenodd" clip-rule="evenodd" image-rendering="optimizeQuality" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" viewBox="0 0 2191.85 1913.6" id="camera"><path fill-rule="nonzero" d="M1630.73 229.46l164.86 0c109.04,0 208.13,44.58 279.91,116.35 71.77,71.77 116.35,170.89 116.35,279.9l0 891.63c0,109.04 -44.57,208.13 -116.34,279.9 -71.77,71.78 -170.88,116.36 -279.92,116.36l-1399.34 0c-109.04,0 -208.13,-44.58 -279.9,-116.36 -71.78,-71.77 -116.36,-170.86 -116.36,-279.9l0 -891.63c0,-109.04 44.58,-208.14 116.36,-279.91 71.77,-71.78 170.86,-116.34 279.9,-116.34l164.87 0c15.58,-50.48 46.02,-94.89 83.46,-130.79 63.66,-61.08 151.05,-98.67 218.71,-98.67l465.25 0c67.66,0 155.06,37.59 218.71,98.67 37.43,35.9 67.87,80.31 83.47,130.79zm-534.81 359.12c133.33,0 254.1,54.07 341.49,141.46 87.4,87.4 141.47,208.16 141.47,341.5 0,133.33 -54.07,254.09 -141.47,341.49 -87.41,87.39 -208.14,141.46 -341.49,141.46 -133.35,0 -254.08,-54.07 -341.49,-141.46 -87.39,-87.41 -141.46,-208.15 -141.46,-341.49 0,-133.35 54.07,-254.09 141.46,-341.5 87.39,-87.39 208.16,-141.46 341.49,-141.46zm236.44 246.52c-60.49,-60.49 -144.09,-97.9 -236.44,-97.9 -92.34,0 -175.95,37.41 -236.44,97.9 -60.47,60.49 -97.9,144.1 -97.9,236.44 0,92.33 37.43,175.95 97.9,236.43 60.49,60.48 144.1,97.91 236.44,97.91 92.33,0 175.95,-37.43 236.44,-97.91 60.49,-60.48 97.9,-144.09 97.9,-236.43 0,-92.35 -37.41,-175.95 -97.9,-236.44zm463.23 -457.03l-227.87 0c-41.03,0 -74.3,-33.27 -74.3,-74.3 0,-36.68 -20.59,-71.15 -48.91,-98.3 -36.67,-35.19 -82.85,-56.85 -115.96,-56.85l-465.25 0c-33.11,0 -79.29,21.66 -115.96,56.85 -28.32,27.16 -48.91,61.62 -48.91,98.3 0,41.03 -33.27,74.3 -74.3,74.3l-227.87 0c-68.04,0 -129.95,27.89 -174.85,72.79 -44.9,44.91 -72.8,106.82 -72.8,174.86l0 891.63c0,68.02 27.9,129.95 72.8,174.85 44.91,44.9 106.82,72.8 174.85,72.8l1399.34 0c68.04,0 129.97,-27.9 174.86,-72.8 44.91,-44.91 72.79,-106.81 72.79,-174.85l0 -891.63c0,-68.02 -27.89,-129.95 -72.8,-174.84 -44.91,-44.91 -106.82,-72.81 -174.85,-72.81z"></path></svg>
    `;
}

function addMenuCard(route, title, imageSrc) {
    var menuCard = document.createElement("div");
    menuCard.className = "bg-white rounded-lg shadow-sm border border-gray-300 overflow-hidden p-4 box-border relative flex flex-col gap-2 justify-between";

    menuCard.innerHTML = `
        <div class="flex flex-col gap-2">
            <div class="w-full h-48 border border-gray-300 rounded-md overflow-hidden">
                <img class="object-cover w-full h-full" src="${imageSrc}" alt="menu card image">
            </div>
            <h3 class="font-bold text-lg text-center">${title}</h3>
        </div>
        
        <a href="${route}" class="font-bold text-white rounded-full bg-blue-500 p-2 text-center flex items-center justify-center gap-3">
            <div class="w-6 h-6">${iconCamera()}</div>
            <span class="hidden sm:inline">Buka Kamera</span>
        </a>
    `;
    
    mainMenu = document.getElementById("main-menu");
    if (mainMenu) mainMenu.appendChild(menuCard);
}

function addMenuCardType(title, imageSrc) {
    var menuCard = document.createElement("div");
    menuCard.className = "bg-white rounded-lg shadow-sm border border-gray-300 overflow-hidden p-4 box-border relative flex flex-col gap-2 justify-between";

    menuCard.innerHTML = `
        <div class="flex flex-col gap-2">
            <div class="w-full h-48 border border-gray-300 rounded-md overflow-hidden">
                <img class="object-cover w-full h-full" src="${imageSrc}" alt="menu card image">
            </div>
            <h3 class="font-bold text-lg text-center">${title}</h3>
        </div>
        
        <a href="${route}" class="font-bold text-white rounded-full bg-blue-500 p-2 text-center flex items-center justify-center gap-3">
            <div class="w-6 h-6">${iconCamera()}</div>
            <span class="hidden sm:inline">Buka Kamera</span>
        </a>
    `;
    
    mainMenu = document.getElementById("main-menu");
    if (mainMenu) mainMenu.appendChild(menuCard);
}

addMenuCard("/craniovertebra", "Craniovertebra Angle", "https://www.researchgate.net/profile/Walaa-Elsayed/publication/347892270/figure/fig1/AS:972676877283329@1608915647914/Measurement-of-Craniovertebral-angle.ppm")

addMenuCard("/forward_shoulder", "Forward Shoulder Angle", "https://www.researchgate.net/profile/Darin-Padua/publication/41122480/figure/fig1/AS:394259766235139@1471010261363/Forward-head-angle-FHA-measured-from-the-vertical-anteriorly-to-a-line-connecting-the.png")

addMenuCard("/carrying", "Carrying Angle", "https://clinicalgate.com/wp-content/uploads/2015/03/F000067f006-008-9781455709779.jpg")

addMenuCard("/q_angle", "Q Angle", "https://www.researchgate.net/profile/Alfred-Atanda/publication/38062380/figure/fig13/AS:394157177753602@1470985802902/The-Q-angle-is-defined-as-the-angle-between-a-line-drawn-from-the-anterior-superior-iliac.png")

addMenuCard("/clark_angle", "Clark Angle", "https://www.researchgate.net/publication/361640780/figure/fig1/AS:11431281172330157@1688505696127/Clarkes-angle-measurement-method-using-footprints-A-the-most-medial-point-of-the.tif")

addMenuCard("/hallux_valgus", "Hallux Valgus Angle", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Hallux_Valgus-Aspect_pr%C3%A9_op_d%C3%A9charge.JPG/800px-Hallux_Valgus-Aspect_pr%C3%A9_op_d%C3%A9charge.JPG")

addMenuCard("/thigh_foot", "Thigh Foot Angle", "")



function saveData(endpoint) {
    let xhr = new XMLHttpRequest();
    // Configure the request
    xhr.open("GET", endpoint, true);

    // Set up event handlers
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            // Successful response handling
            // console.log(xhr.responseText);
            alert("Data berhasil direkam");
        } else {
            // Error response handling
            // console.error("Error in API call:", xhr.status, xhr.statusText);
            alert("Terjadi kesalahan saat merekam data");
        }
    };

    xhr.onerror = function () {
        // Network error handling
        console.error("Network error occurred");
        alert("Terjadi kesalahan saat merekam data");
    };

    // Send the request
    xhr.send(); 
}

var currEndpoint = window.location.pathname;

if (currEndpoint == "/carrying") {
    document.getElementById("btn_save_carry").addEventListener("click", function() {
        saveData("/save_carry")
    });
}
if (currEndpoint == "/craniovertebra") {
    document.getElementById("btn_save_cv").addEventListener("click", function() {
        saveData("/save_cv")
    });
}
if (currEndpoint == "/forward_shoulder") {
    document.getElementById("btn_save_fsa").addEventListener("click", function() {
        saveData("/save_fsa")
    });
}
if (currEndpoint == "/q_angle") {
    document.getElementById("btn_save_q").addEventListener("click", function() {
        saveData("/save_q")
    });
}
if (currEndpoint == "/clark_angle") {
    document.getElementById("btn_save_clark").addEventListener("click", function() {
        saveData("/save_clark")
    });
}
if (currEndpoint == "/hallux_valgus") {
    document.getElementById("btn_save_hallux").addEventListener("click", function() {
        saveData("/save_hallux")
    });
}