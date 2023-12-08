const renderWeeklyChart = (mondata,tuedata,weddata,thudata,fridata,satdata,sundata) => {
const ctx = document.getElementById('myChartWeekly').getContext('2d');
const myChartWeekly = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Перерывы', 'Задачи', 'Встречи'],
        datasets: [
            
            {
                label: 'Понедельник',
                data: mondata,
                backgroundColor: [
                    'rgba(0, 255, 0, 0.2)',
                    'rgba(0, 255, 0, 0.2)',
                    'rgba(0, 255, 0, 0.2)'
                ],
                borderColor: [
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)'
                ],
                borderWidth: 1
            },
    
    
    
    
    
            {
                label: 'Вторник',
                data: tuedata,
                backgroundColor: [
                    'rgba(0, 0, 255, 0.2)',
                    'rgba(0, 0, 255, 0.2)',
                    'rgba(0, 0, 255, 0.2)'
                    
                ],
                borderColor: [
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)'
                ],
                borderWidth: 1
            },
    
    
    
            {
                label: 'Среда',
                data: weddata,
                backgroundColor: [
                    'rgba(220, 20, 60, 0.2)',
                    'rgba(220, 20, 60, 0.2)',
                    'rgba(220, 20, 60, 0.2)'
                ],
                borderColor: [
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)'
                ],
                borderWidth: 1
            },
    
    
    
            {
                label: 'Четверг',
                data: thudata,
                backgroundColor: [
                    'rgba(255, 140, 0, 0.2)',
                    'rgba(255, 140, 0, 0.2)',
                    'rgba(255, 140, 0, 0.2)'
                    
                ],
                borderColor: [
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)'
                ],
                borderWidth: 1
            },
        
    
    
    
            {
                label: 'Пятница',
                data: fridata,
                backgroundColor: [
                    'rgba(255, 0, 0, 0.2)',
                    'rgba(255, 0, 0, 0.2)',
                    'rgba(255, 0, 0, 0.2)'
                    
                ],
                borderColor: [
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)'
                ],
                borderWidth: 1
            },
    
    
            {
                label: 'Суббота',
                data: satdata,
                backgroundColor: [
                    'rgba(173, 216, 230, 0.2)',
                    'rgba(173, 216, 230, 0.2)',
                    'rgba(173, 216, 230, 0.2)'
                    
                ],
                borderColor: [
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)'
                ],
                borderWidth: 1
            },
    
    
    
            {
                label: 'Воскресенье',
                data: sundata,
                backgroundColor: [
                    'rgba(255, 0, 255, 0.2)',
                    'rgba(255, 0, 255, 0.2)',
                    'rgba(255, 0, 255, 0.2)'
                    
                ],
                borderColor: [
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)',
                    'rgba(0, 0, 0, 1)'
                ],
                borderWidth: 1
            },
    
    
    
    
    ]
    },
    options: {
        scales: {
            yAxes: [{ ticks:{beginAtZero:true},stacked: true}],
            xAxes: [{stacked: true}]
        }
    }
});
};





const getWeeklyChartData = () => {
    fetch("Aget_weekly_tasks")
      .then((res) => res.json())
      .then((Wresults) => {
        
        const WMONDAY = Wresults.MONDAY;
        const WTUESDAY = Wresults.TUESDAY;
        const WWEDNESDAY = Wresults.WEDNESDAY;
        const WTHURSDAY = Wresults.THURSDAY;
        const WFRIDAY = Wresults.FRIDAY;
        const WSATURDAY = Wresults.SATURDAY;
        const WSUNDAY = Wresults.SUNDAY;
        const [mondata] = [Object.values(WMONDAY)];
        const [tuedata] = [Object.values(WTUESDAY)];
        const [weddata] = [Object.values(WWEDNESDAY)];
        const [thudata] = [Object.values(WTHURSDAY)];
        const [fridata] = [Object.values(WFRIDAY)];
        const [satdata] = [Object.values(WSATURDAY)];
        const [sundata] = [Object.values(WSUNDAY)];
        renderWeeklyChart(mondata,tuedata,weddata,thudata,fridata,satdata,sundata);
        });
  };
  
  document.onload = getWeeklyChartData();
