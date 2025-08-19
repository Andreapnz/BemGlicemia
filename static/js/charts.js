function renderGlucoseChart(canvasId, labels, values) {
  const ctx = document.getElementById(canvasId).getContext('2d');

  // Converte "DD/MM/YYYY HH:mm" para "DD/MM/YYYY - HH:mm"
  function formatDateLabel(d) {
    const [datePart, timePart] = d.split(" ");
    return `${datePart} - ${timePart}`;
  }

  const formattedLabels = labels.map(formatDateLabel);

  const data = {
    labels: formattedLabels,
    datasets: [{
      label: 'Glicemia (mg/dL)',
      data: values,
      fill: true,
      tension: 0.35,
      pointRadius: 4,
      borderWidth: 2
    }]
  };

  const normalMin = 70, normalMax = 180;

  const chart = new Chart(ctx, {
    type: 'line',
    data,
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      interaction: { mode: 'nearest', intersect: false },
      scales: {
        x: {
          type: 'category', // mantém a label exatamente como string
          ticks: { autoSkip: true, maxTicksLimit: 8 }
        },
        y: { title: { display: true, text: 'mg/dL' } }
      }
    },
    plugins: [{
      id: 'normalBand',
      afterDraw(c) {
        const { ctx, chartArea, scales } = c;
        const y1 = scales.y.getPixelForValue(normalMax);
        const y2 = scales.y.getPixelForValue(normalMin);
        ctx.save();
        ctx.globalAlpha = 0.10;
        ctx.fillStyle = 'green';
        ctx.fillRect(chartArea.left, Math.min(y1, y2), chartArea.right - chartArea.left, Math.abs(y2 - y1));
        ctx.restore();
      }
    }]
  });

  return chart;
}
