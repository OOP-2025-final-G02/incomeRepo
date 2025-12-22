const canvas = document.getElementById('chart3');
const ctx = canvas.getContext('2d');

const products = JSON.parse(
  document.getElementById('products-data').textContent
);

// ★ 日付でソート（重要）
products.sort((a, b) => {
  return new Date(a.created_at) - new Date(b.created_at);
});

// 年一覧（重複なし・昇順）
const years = [...new Set(
  products.map(p => new Date(p.created_at).getFullYear())
)].sort();

const yearSelect = document.getElementById('yearSelect');

// プルダウン作成
years.forEach(year => {
  const option = document.createElement('option');
  option.value = year;
  option.textContent = year + '年';
  yearSelect.appendChild(option);
});

let chart;

// グラフ描画
function drawChart(selectedYear) {
  const labels = [];
  const incomes = [];

  // 年で絞り込み（ソート済み）
  const filtered = products.filter(p =>
    new Date(p.created_at).getFullYear() === selectedYear
  );

  // 月別集計
  filtered.forEach(p => {
    const d = new Date(p.created_at);
    const monthLabel = (d.getMonth() + 1) + '月';
    const income = Number(p.income);

    const index = labels.indexOf(monthLabel);

    if (index === -1) {
      labels.push(monthLabel);
      incomes.push(income);
    } else {
      incomes[index] += income;
    }
  });

  // ★ 平均収入
  const average =
    incomes.reduce((sum, v) => sum + v, 0) / incomes.length;

  // ★ 平均との差
  const diffFromAvg = incomes.map(v => v - average);

  // 既存グラフ破棄
  if (chart) {
    chart.destroy();
  }

  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: `${selectedYear}年（月平均との差）｜平均収入：${average.toFixed(0)}円`,
        data: diffFromAvg
      }]
    }
  });
}

// 初期表示
drawChart(years[0]);

// 年変更時
yearSelect.addEventListener('change', () => {
  drawChart(Number(yearSelect.value));
});
