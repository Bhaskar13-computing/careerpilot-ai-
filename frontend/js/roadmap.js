const generateBtn = document.getElementById("generateBtn");
const roadmapContainer = document.getElementById("roadmapContainer");

generateBtn.addEventListener("click", async () => {
  const name = document.getElementById("name").value.trim();
  const branch = document.getElementById("branch").value;
  const year = document.getElementById("year").value;
  const interest = document.getElementById("interest").value;

  // Basic validation
  if (!name || !branch || !year || !interest) {
    roadmapContainer.innerHTML =
      "<p class='placeholder'>Please fill all fields.</p>";
    return;
  }

  roadmapContainer.innerHTML =
    "<p class='placeholder'>Generating roadmap...</p>";

  try {
    const response = await fetch("http://127.0.0.1:5000/get-roadmap", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        branch: branch,
        year: year,
        interest: interest
      })
    });

    if (!response.ok) {
      throw new Error("No roadmap found");
    }

    const data = await response.json();
    const roadmap = data.roadmap;

    // Render roadmap
    roadmapContainer.innerHTML = `<p><strong>Hey ${name}, here’s your roadmap 👇</strong></p>`;

    roadmap.forEach(step => {
      const stepDiv = document.createElement("div");
      stepDiv.className = "roadmap-step";

      stepDiv.innerHTML = `
        <h3>Step ${step.step}: ${step.title}</h3>
        <p><strong>What to learn:</strong> ${step.learn.join(", ")}</p>
        <p><strong>Skills:</strong> ${step.skills.join(", ")}</p>
        <p><strong>Tools:</strong> ${step.tools.join(", ")}</p>
        <p><strong>Outcome:</strong> ${step.outcome}</p>
      `;

      roadmapContainer.appendChild(stepDiv);
    });

  } catch (error) {
    roadmapContainer.innerHTML =
      "<p class='placeholder'>No roadmap available for selected options.</p>";
  }
});
