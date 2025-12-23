const ctx = document.getElementById('chart3').getContext('2d');

// ===== データ読み込み =====
const products = JSON.parse(
  document.getElementById('products-data').textContent
);

const users = JSON.parse(
  document.getElementById('users-data').textContent
);

// 日付でソート
products.sort((a, b) => {
  return new Date(a.created_at) - new Date(b.created_at);
});

// ===== user_id → user_name の対応表 =====
const userNameMap = {};
users.forEach(u => {
  userNameMap[u.id] = u.name;
});

// ===== セレクト要素 =====
const yearSelect = document.getElementById('yearSelect');
const userSelect = document.getElementById('userSelect');

// ===== 年一覧 =====
const years = [...new Set(
  products.map(p => new Date(p.created_at).getFullYear())
)].sort();

// ===== ユーザー一覧 =====
const userIds = [...new Set(
  products.map(p => p.user_id)
)];

// 年プルダウン
years.forEach(year => {
  const opt = document.createElement('option');
  opt.value = year;
  opt.textContent = year + '年';
  yearSelect.appendChild(opt);
});

// ユーザープルダウン（名前表示）
userIds.forEach(id => {
  const opt = document.createElement('option');
  opt.value = id;
  opt.textContent = userNameMap[id];
  userSelect.appendChild(opt);
});

let chart;

// ===== グラフ描画 =====
function drawChart(year, userId) {
  const labels = [];
  const incomes = [];

  // 年 × ユーザーで絞り込み
  const filtered = products.filter(p =>
    new Date(p.created_at).getFullYear() === year &&
    p.user_id === userId
  );

  // 月別集計
  filtered.forEach(p => {
    const d = new Date(p.created_at);
    const month = (d.getMonth() + 1) + '月';
    const income = Number(p.income);

    const idx = labels.indexOf(month);
    if (idx === -1) {
      labels.push(month);
      incomes.push(income);
    } else {
      incomes[idx] += income;
    }
  });

  // データなし対策
  if (incomes.length === 0) {
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [{
          label: `${year}年 ${userNameMap[userId]}（データなし）`,
          data: []
        }]
      }
    });
    return;
  }

  // 平均
  const average =
    incomes.reduce((sum, v) => sum + v, 0) / incomes.length;

  // 平均差
  const diff = incomes.map(v => v - average);

  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: `${year}年 ${userNameMap[userId]}｜平均との差（平均：${average.toFixed(0)}円）`,
        data: diff
      }]
    }
  });
}

// ===== セレクト変更時 =====
function tryDraw() {
  if (!yearSelect.value || !userSelect.value) return;
  drawChart(Number(yearSelect.value), Number(userSelect.value));
}

yearSelect.addEventListener('change', tryDraw);
userSelect.addEventListener('change', tryDraw);

// 初期表示
drawChart(years[0], userIds[0]);
