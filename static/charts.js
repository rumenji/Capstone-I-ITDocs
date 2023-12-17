const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const COUNT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

const dateCurrent = new Date(Date.now());
const currentMonth = dateCurrent.getMonth();
const todayDate = dateCurrent.getDate();

$ticketsToday = $('#tickets_today');
$ticketsMtd = $('#tickets_mtd');
$ticketsYtd = $('#tickets_ytd');
$ticketsOpen = $('#tickets_open');

$(document).ready(function () {
    getDeskStats();
    });
    
let chartData = {};

let ticketsYTD = 0;
let ticketsMonth = 0;
let ticketsToday = 0;

let newMntLables = [];
let newMntValues = [];

let openTickets = 0;
let closedTickets = 0;

let ticketsAssignee = {};
let assigneeNameList = [];
let assigneeOpenTickets = [];
let assigneeClosedTickets = [];

async function getDeskStats() {
    const deskStats = await axios.get('/desk/stats');
    chartData = deskStats.data;
    ticketsYTD = chartData.length;
    getMonthLabelsValues(chartData)
    getMonthTodayTickets(chartData)
    getByStatus(chartData)
    getByAssignees(chartData)
    plotYTDChart()
    plotOpenChart()
    plotUserChart()
    setTicketStatValues()
};

function getMonthLabelsValues(stats){
    newMntLables = MONTHS.slice(0, currentMonth+1)
    
    for(let ticket of stats){
        const dateTicket = new Date(ticket.timestamp);
        const ticketMonth = dateTicket.getMonth();
        if(newMntValues[ticketMonth]){
            newMntValues[ticketMonth] += 1;
        } else {
            newMntValues[ticketMonth] = 1;
        }
    for(let i=0; i<currentMonth ;i++){
        if(newMntValues[i] !== Number){
            newMntValues[i] = 0;
        }
    }    
    }
}

function getMonthTodayTickets(stats){
    for(let ticket of stats){
        const dateTicket = new Date(ticket.timestamp);
        const ticketMonth = dateTicket.getMonth();
        const ticketDate = dateTicket.getDate();
        if(ticketMonth === currentMonth){
            ticketsMonth++;
        }
        if(ticketDate === todayDate){
            ticketsToday++;
        }
    }
}

function getByStatus(stats) {
    for(let ticket of stats){
        if(ticket.status === true){
            closedTickets++;
        } else {
            openTickets++;
        }
    
}
}

function getByAssignees(stats){
    for(let ticket of stats){
        if(ticket.user in ticketsAssignee){
            if(ticket.status === true){
                ticketsAssignee[ticket.user]['Closed'] += 1;
            } else {
                ticketsAssignee[ticket.user]['Open'] += 1;
            }
        } else {
            if(ticket.status === true){
                ticketsAssignee[ticket.user] = {'Closed': 1, 'Open': 0}
            } else {
                ticketsAssignee[ticket.user] = {'Closed': 0, 'Open': 1}
            }
        }
    }
    assigneeNameList = Object.keys(ticketsAssignee)
    for(let user of assigneeNameList){
        assigneeClosedTickets.push(ticketsAssignee[user]['Closed'])
        assigneeOpenTickets.push(ticketsAssignee[user]['Open'])
    }
}
// async function getYTDStats() {
//     const ytdStats = await axios.get('/desk/ytd_tickets');
    
// };

function plotYTDChart() {
    const data = {
        labels: newMntLables,
        datasets: [{
            label: 'Ticket volume',
            backgroundColor: 'rgb(196, 30, 58)',
            borderColor: 'rgb(255, 99, 132)',
            data: newMntValues,
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: { maintainAspectRatio: true, 
                    responsive: true, scales: {
                        y: {
                            ticks: {
                                precision: 0
                            }
                        }
                    } }
    };

    const ticketVolumeChart = new Chart(
        document.getElementById('ticketVolumeChart'),
        config
    );

}

// async function getOpenStats() {
//     const openStats = await axios.get('/desk/open_tickets');
//     plotOpenChart(openStats.data)
// };

function plotOpenChart() {
    
    const statusLabels = ['Closed', 'Open']
    const statusValues = [closedTickets, openTickets]
    
    const data = {
        labels: statusLabels,
        datasets: [{
            label: 'Tickets by status',
            backgroundColor: ['rgb(196, 30, 58)', 'rgb(0,128,0)'],
            hoverOffset: 4,
            data: statusValues
        }]
    };

    const config = {
        type: 'doughnut',
        data: data
    };

    const ticketByStatusChart = new Chart(
        document.getElementById('ticketByStatusChart'),
        config
    );

}

// async function getByUser() {
//     const userStats = await axios.get('/desk/tickets_user');
//     plotUserChart(userStats.data)
// };

function plotUserChart() {
    
    const data = {
        labels: assigneeNameList,
        datasets: [{
            label: 'Closed',
            backgroundColor: ['rgb(196, 30, 58)'],
            hoverOffset: 4,
            data: assigneeClosedTickets
        },
        {
            label: 'Open',
            backgroundColor: ['rgb(0,128,0)'],
            hoverOffset: 4,
            data: assigneeOpenTickets
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options:{
            indexAxis: 'y',
            scales: {
                y: {
                    stacked:true
                },
                x: {
                    ticks: {
                        precision: 0
                    },
                    stacked: true
                }
            }    
        }
        
    };

    const ticketAssigneeChart = new Chart(
        document.getElementById('ticketAssigneeChart'),
        config
    );

}

function setTicketStatValues(){
    $ticketsToday.text(ticketsToday);
    $ticketsMtd.text(ticketsMonth);
    $ticketsYtd.text(ticketsYTD);
    $ticketsOpen.text(openTickets);
}
