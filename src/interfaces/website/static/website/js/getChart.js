const getChart = (chartId, chartDataId) => {
  const chartSelector = document.getElementById(chartId);
  const chartDataSelector = document.getElementById(chartDataId);
  const chartDataConfig = JSON.parse(chartDataSelector.textContent);
  return new Chart(chartSelector, chartDataConfig);
}