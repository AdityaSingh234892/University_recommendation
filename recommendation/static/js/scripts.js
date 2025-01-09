document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const resultDiv = document.getElementById("recommendation-result");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        // Clear previous results and show a loading message
        resultDiv.innerHTML = "<p>Loading recommendations...</p>";

        const formData = new FormData(form);

        try {
            // Send the form data to the server
            const response = await fetch("/", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const result = await response.json();

            if (result.recommendation) {
                // Parse and clean the recommendation data
                const lines = result.recommendation
                    .split("\n")
                    .filter((line) => line.trim() !== "" && !line.startsWith("---")); // Remove separator lines

                // Manually define headers
                const tableHeaders = ["University Name", "Fees", "Ranking", "Location"];

                // Extract and process rows of data
                const rows = lines.map((line) => {
                    return line.split(/\s{2,}|\t+/).map((cell) => cell.trim());
                });

                // Ensure exactly 10 rows
                if (rows.length !== 10) {
                    resultDiv.innerHTML = `<p>Error: Expected exactly 10 universities, but found ${rows.length}.</p>`;
                    return;
                }

                // Build the HTML table
                let tableHTML = `<h2>Recommendations</h2><table border="1"><thead><tr>`;
                tableHeaders.forEach((header) => {
                    tableHTML += `<th>${header}</th>`;
                });
                tableHTML += `</tr></thead><tbody>`;

                rows.forEach((row) => {
                    if (row.length === 4) { // Ensure the row has exactly 4 columns
                        tableHTML += `<tr>`;
                        row.forEach((cell) => {
                            tableHTML += `<td>${cell}</td>`;
                        });
                        tableHTML += `</tr>`;
                    }
                });

                tableHTML += `</tbody></table>`;

                // Render the table in the resultDiv
                resultDiv.innerHTML = tableHTML;
            } else {
                resultDiv.innerHTML = `<p>Error: No recommendations received.</p>`;
            }
        } catch (error) {
            console.error("Error fetching recommendations:", error);
            resultDiv.innerHTML = "<p>An error occurred while fetching recommendations. Please try again later.</p>";
        }
    });
}); 