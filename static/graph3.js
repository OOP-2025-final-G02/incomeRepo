const canvas = document.getElementById('chart3');
  
    const products = JSON.parse(
    document.getElementById('products-data').textContent
    );
    products.sort((a, b) => {
      return new Date(a.created_at) - new Date(b.created_at);
    });
  
    const labels = [];
    const incomes = [];
  
    products.forEach(p => {
      const d = new Date(p.created_at);
      labels.push((d.getMonth() + 1) + '月');
      incomes.push(Number(p.income));
    });
  
    const avg = incomes.reduce((a, b) => a + b, 0) / incomes.length;
    const diffs = incomes.map(v => v - avg);
    const avgText = Math.round(avg).toLocaleString();
  
    new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: `平均との差（平均：${avgText} 円）`,
          data: diffs
        }]
      }
    });