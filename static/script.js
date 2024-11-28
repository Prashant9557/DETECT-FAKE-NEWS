document.addEventListener("DOMContentLoaded", () => {
  const predictButton = document.querySelector(".submit-btn");
  const urlInput = document.querySelector(".input-field"); // Input field for the URL
  const resultSection = document.querySelector(".result-section"); // Result display area

  // Hide result section initially
  resultSection.style.display = "none";

  // Add event listener to the prediction button
  predictButton.addEventListener("click", async (event) => {
    event.preventDefault(); // Prevent default form submission behavior
    const url = urlInput.value.trim();

    // Validate URL input
    if (!url) {
      alert("Please enter a valid URL.");
      return;
    }

    try {
      // Display loading indication
      resultSection.style.display = "block";
      resultSection.innerHTML = "<p>Loading prediction...</p>";

      // Make the API call to the Flask backend for prediction
      const response = await fetch("http://127.0.0.1:5000/prediction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
      });

      // Check if the response is not OK (e.g., 404, 500)
      if (!response.ok) {
        const errorData = await response.json();
        resultSection.innerHTML = `<p>Error: ${
          errorData.error || "Something went wrong."
        }</p>`;
        return;
      }

      // If response is valid JSON
      const data = await response.json();

      // Display the prediction result and confidence score
      if (data.prediction && data.confidence_score) {
        const predictionStyle =
          data.prediction.toLowerCase() === "real"
            ? "color: green; font-weight: bold; font-size: 1.5rem;" // Style for "Real"
            : "color: red; font-weight: bold; font-size: 1.5rem;"; // Style for "Fake"

        // Update the result section with prediction and confidence
        resultSection.innerHTML = `
          <p><strong>Prediction:</strong> <span style="${predictionStyle}">${data.prediction}</span></p>
          <p><strong>Confidence:</strong> ${data.confidence_score}%</p>
          <canvas id="confidenceChart" width="400" height="200"></canvas>
        `;

        // Prepare data for the chart
        const modelLabels = Object.keys(data.model_scores); // e.g., ["Logistic Regression", "Gradient Boosting", ...]
        const modelScores = Object.values(data.model_scores); // e.g., [85.3, 90.5, ...]

        // Render the chart using Chart.js
        const ctx = document.getElementById("confidenceChart").getContext("2d");
        new Chart(ctx, {
          type: "bar", // Bar chart
          data: {
            labels: modelLabels,
            datasets: [
              {
                label: "Model Confidence Scores (%)",
                data: modelScores,
                backgroundColor: [
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(255, 159, 64, 0.2)",
                  "rgba(255, 99, 132, 0.2)",
                ],
                borderColor: [
                  "rgba(75, 192, 192, 1)",
                  "rgba(153, 102, 255, 1)",
                  "rgba(255, 159, 64, 1)",
                  "rgba(255, 99, 132, 1)",
                ],
                borderWidth: 1,
              },
            ],
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
              },
            },
          },
        });
      } else {
        resultSection.innerHTML =
          "<p>Unable to process the response correctly. Please try again.</p>";
      }
    } catch (error) {
      console.error("Error occurred:", error);
      resultSection.innerHTML =
        "<p>Failed to connect to the server. Please try again later.</p>";
    }
  });
});
