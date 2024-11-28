document.addEventListener("DOMContentLoaded", () => {
  const analyzeBtn = document.getElementById("analyzeBtn");
  const urlInput = document.getElementById("urlInput");
  const resultDiv = document.getElementById("result");

  analyzeBtn.addEventListener("click", async () => {
    const url = urlInput.value.trim();
    if (!url) {
      resultDiv.innerHTML =
        "<p style='color: red;'>Please enter a valid URL.</p>";
      return;
    }

    try {
      resultDiv.innerHTML = "<p>Analyzing...</p>";

      const response = await fetch("http://127.0.0.1:5000/prediction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Source": "chrome-extension",
        },
        body: JSON.stringify({ url: url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        resultDiv.innerHTML = `<p style='color: red;'>Error: ${
          errorData.error || "Something went wrong."
        }</p>`;
        return;
      }

      const data = await response.json();
      const color = data.prediction.toLowerCase() === "real" ? "green" : "red";
      resultDiv.innerHTML = `
                <p><strong>Prediction:</strong> <span style="color: ${color};">${data.prediction}</span></p>
                <p><strong>Confidence:</strong> ${data.confidence_score}%</p>
            `;
    } catch (error) {
      resultDiv.innerHTML =
        "<p style='color: red;'>Failed to connect to the server.</p>";
      console.error("Error:", error);
    }
  });
});
