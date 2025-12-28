document.addEventListener("DOMContentLoaded", function () {
  const valveCards = document.querySelectorAll(".valve-card");
  const modal = document.getElementById("valve-modal");
  const closeBtn = document.querySelector(".close-btn");
  const modalTitle = document.getElementById("modal-title");
  const valveForm = document.getElementById("valve-form");

  let currentRelayStates = [];

  // Open Modal
  valveCards.forEach((card) => {
    card.addEventListener("click", function () {
      const valveId = this.id.split("-").pop();
      const valveName = this.querySelector("h3").innerText;

      document.getElementById("relay-id").value = valveId;
      modalTitle.innerText = `Cài đặt ${valveName}`;

      const relay = currentRelayStates.find((r) => r.relay_id == valveId);
      const modeSelect = document.getElementById("valve-mode");
      const manualControls = document.getElementById("manual-controls");
      const toggleBtn = document.getElementById("toggle-valve-btn");

      if (relay) {
        // Set Mode
        // Map DB value 'Tự động'/'Thủ công' or 'auto'/'manual' to select values 'auto'/'manual'
        const modeLower = (relay.mode || "").toLowerCase();
        if (modeLower.includes("tự động") || modeLower === "auto") {
          modeSelect.value = "auto";
          manualControls.style.display = "none";
        } else {
          modeSelect.value = "manual";
          manualControls.style.display = "block";

          // Update Toggle Button Text/Style based on state
          const stateLower = (relay.state || "").toLowerCase();
          if (stateLower === "on") {
            toggleBtn.innerText = "Tắt";
            toggleBtn.style.backgroundColor = "var(--danger-color)";
            toggleBtn.style.border = "1px solid var(--danger-color)";
          } else {
            toggleBtn.innerText = "Bật";
            toggleBtn.style.backgroundColor = "var(--secondary-color)";
            toggleBtn.style.border = "1px solid var(--secondary-color)";
          }
        }
      }

      modal.classList.remove("hidden");
    });
  });

  // Handle Mode Change in Modal
  const modeSelect = document.getElementById("valve-mode");
  if (modeSelect) {
    modeSelect.addEventListener("change", function () {
      const manualControls = document.getElementById("manual-controls");
      if (this.value === "manual") {
        manualControls.style.display = "block";
      } else {
        manualControls.style.display = "none";
      }
    });
  }

  // Handle Toggle Button Click
  const toggleBtn = document.getElementById("toggle-valve-btn");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
      const valveId = document.getElementById("relay-id").value;
      if (!valveId) return;

      const relay = currentRelayStates.find((r) => r.relay_id == valveId);
      if (!relay) return;

      const currentState = (relay.state || "").toLowerCase();
      const newState = currentState === "on" ? "off" : "on";

      fetch("/api/update_relay_state_db", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          relay_id: valveId,
          state: newState.toUpperCase(),
        }), // Send uppercase usually
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("Toggled state", data);
          // Optimistic UI update or wait for polling
          updateValveStates(); // Force update immediately
          modal.classList.add("hidden");
        })
        .catch((err) => console.error("Error toggling valve:", err));
    });
  }

  // Close Modal Button
  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      modal.classList.add("hidden");
    });
  }

  // Close on Clicking Outside
  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        modal.classList.add("hidden");
      }
    });
  }

  // Handle Form Submit (Save Mode)
  if (valveForm) {
    valveForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const mode = document.getElementById("valve-mode").value;
      const valveId = document.getElementById("relay-id").value;
      // Convert select value 'auto'/'manual' to DB value if needed,
      // but simpler to use consistent values. Let's send 'Tự động'/'Thủ công' if backend expects that,
      // OR just 'auto'/'manual' if backend handles it.
      // Based on init_db, it used 'Tự động'. let's map it.

      const dbMode = mode === "auto" ? "Tự động" : "Thủ công";

      fetch("/api/update_relay_mode_db", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ relay_id: valveId, mode: dbMode }),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(`Saved mode for Valve ${valveId}: ${dbMode}`);
          updateValveStates();
          modal.classList.add("hidden");
        })
        .catch((error) => console.error("Error saving mode:", error));
    });
  }

  // Fetch and update Sensor Data
  function updateSensorData() {
    fetch("/api/latest_luuluong_1_2_and_total")
      .then((response) => response.json())
      .then((data) => {
        // Update values if elements exist
        const luuLuong1 = document.getElementById("LuuLuong1");
        const luuLuong2 = document.getElementById("LuuLuong2");
        const luuLuongTong = document.getElementById("LuuLuongTong");

        if (luuLuong1 && data.luu_luong_1) {
          const content = data.luu_luong_1.TongLuuLuong || "--";
          luuLuong1.innerText = content + " L/P";
        }
        if (luuLuong2 && data.luu_luong_2) {
          const content = data.luu_luong_2.TongLuuLuong || "--";
          luuLuong2.innerText = content + " L/P";
        }
        if (luuLuongTong) {
          const content = data.tong_luu_luong || "--";
          luuLuongTong.innerText = content + " L/P";
        }
      })
      .catch((error) => console.error("Error fetching flow data:", error));

    // Fetch Pressure
    fetch("/api/latest_apxuat")
      .then((response) => response.json())
      .then((data) => {
        const el = document.getElementById("ApXuat");
        if (el) el.innerText = (data !== null ? data : "--") + " bar";
      })
      .catch((error) => console.error("Error fetching pressure:", error));

    // Fetch EC
    fetch("/api/latest_ec")
      .then((response) => response.json())
      .then((data) => {
        const el = document.getElementById("EC");
        if (el) el.innerText = (data !== null ? data : "--") + " mS/cm";
      })
      .catch((error) => console.error("Error fetching EC:", error));

    // Fetch pH
    fetch("/api/latest_ph")
      .then((response) => response.json())
      .then((data) => {
        const el = document.getElementById("PH");

        if (el) el.innerText = (data !== null ? data.toFixed(2) : "--") + " pH";
      })
      .catch((error) => console.error("Error fetching pH:", error));
  }

  // Fetch Valve States
  function updateValveStates() {
    fetch("/api/relay_state")
      .then((response) => response.json())
      .then((data) => {
        // Update global cache
        currentRelayStates = data;

        // data is expected to be an array of objects: [{relay_id: 1, state: 'on'}, ...]
        data.forEach((relay) => {
          const led = document.getElementById(`led-${relay.relay_id}`);
          if (led) {
            const state = (relay.state || "").toLowerCase();
            if (state === "on") {
              led.style.backgroundColor = "var(--secondary-color)"; // Green for ON
              led.style.boxShadow = "0 0 10px rgba(52, 211, 153, 0.5)";
            } else {
              led.style.backgroundColor = "var(--danger-color)"; // Red for OFF
              led.style.boxShadow = "0 0 10px rgba(248, 113, 113, 0.5)";
            }
          }
        });
      })
      .catch((error) =>
        console.error("Error fetching valve/relay states:", error)
      );
  }

  // Initial call and periodic update
  updateSensorData();
  updateValveStates();
  setInterval(() => {
    updateSensorData();
    updateValveStates();
  }, 3000);
});
