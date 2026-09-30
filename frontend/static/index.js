const timeDisplay = document.getElementById("server-time");
const visitCountElement = document.getElementById("visit-count");
const capitalElement = document.getElementById("user-capital");

async function userVisits() {
    try {
        const response = await fetch("/api/visit", { method: "POST" });
        if (!response.ok) throw new Error("Failed to update visit count");
        
        const data = await response.json();
        if (visitCountElement) {
            visitCountElement.innerText = `Page Visits: ${data.visits}`;
        }
    } catch (error) {
        console.error("Error recording page visit:", error);
    }
}

async function getTime() {
    if (!timeDisplay) return;
    try {
        const res = await fetch("/api/time");
        const data = await res.json();
        timeDisplay.innerText = new Date(data.serverTime).toLocaleString("fi-FI", {
            year: "numeric", month: "2-digit", day: "2-digit",
            hour: "2-digit", minute: "2-digit", second: "2-digit"
        });
    } catch {
        timeDisplay.innerText = "Unable to fetch time";
    }
}

async function getCapital() {
    if (!capitalElement) return;
    try {
        const ipResponse = await fetch("https://ipapi.co/json/");
        const ipData = await ipResponse.json();
        const userLocation = ipData.country_name;

        capitalElement.textContent = `Ip location: ${userLocation}. Your capital is...`;

        const userCapital = await fetch(`/api/capital?country=${encodeURIComponent(userLocation)}`);
        const capitalData = await userCapital.json();

        if (capitalData.capital) {
            capitalElement.textContent = `Ip location: ${userLocation}. Your capital is ${capitalData.capital}`;
        } else {
            capitalElement.textContent = "Could not find your capital";
        }
    } catch (error) {
        console.error("Error fetching capital:", error);
    }
}

getTime();
userVisits();
getCapital();