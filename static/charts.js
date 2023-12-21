/*
Sends a GET request to the ticket_stats routeto get all tickets for the current year and plots the charts for the dashboard.
Included in home_desk.html.
*/

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const COUNT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

// Save today's date, current month and year
const dateCurrent = new Date(Date.now());
const currentMonth = dateCurrent.getMonth();
const todayDate = dateCurrent.getDate();

// Stat fields on the dashboard to be updated
$ticketsToday = $('#tickets_today');
$ticketsMtd = $('#tickets_mtd');
$ticketsYtd = $('#tickets_ytd');
$ticketsOpen = $('#tickets_open');


$(document).ready(function () {
    getDeskStats();
});

// Values needed to be passed to the chart plotting functions
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
    // Sends a GET request to get all tickets for the current year. Calls the value claculation and plotting functions.
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


function getMonthLabelsValues(stats) {
    // Slices the array of all months up to the current. Gets values per month. Fills the months with no tickets with 0.
    newMntLables = MONTHS.slice(0, currentMonth + 1)

    for (let ticket of stats) {
        const dateTicket = new Date(ticket.timestamp);
        const ticketMonth = dateTicket.getMonth();
        if (newMntValues[ticketMonth]) {
            newMntValues[ticketMonth] += 1;
        } else {
            newMntValues[ticketMonth] = 1;
        }
    }
    for (let i = 0; i < currentMonth; i++) {
        if (typeof newMntValues[i] !== 'number') {
            newMntValues[i] = 0;
        }
    }
}

function getMonthTodayTickets(stats) {
    // Loops over all tickets to find the ones from the current date and month.
    for (let ticket of stats) {
        const dateTicket = new Date(ticket.timestamp);
        const ticketMonth = dateTicket.getMonth();
        const ticketDate = dateTicket.getDate();
        if (ticketMonth === currentMonth) {
            ticketsMonth++;
        }
        if (ticketDate === todayDate) {
            ticketsToday++;
        }
    }
}

function getByStatus(stats) {
    // Loops over all tickets to find tickets by open and closed.
    for (let ticket of stats) {
        if (ticket.status === true) {
            closedTickets++;
        } else {
            openTickets++;
        }

    }
}

function getByAssignees(stats) {
    // Loops over all tickets to find tickets by assignee.
    for (let ticket of stats) {
        if (ticket.user in ticketsAssignee) {
            if (ticket.status === true) {
                ticketsAssignee[ticket.user]['Closed'] += 1;
            } else {
                ticketsAssignee[ticket.user]['Open'] += 1;
            }
        } else {
            if (ticket.status === true) {
                ticketsAssignee[ticket.user] = { 'Closed': 1, 'Open': 0 }
            } else {
                ticketsAssignee[ticket.user] = { 'Closed': 0, 'Open': 1 }
            }
        }
    }
    assigneeNameList = Object.keys(ticketsAssignee)
    for (let user of assigneeNameList) {
        assigneeClosedTickets.push(ticketsAssignee[user]['Closed'])
        assigneeOpenTickets.push(ticketsAssignee[user]['Open'])
    }
}


function plotYTDChart() {
    // Plots the tickets YTD line chart
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
        options: {
            maintainAspectRatio: true,
            responsive: true,
            scales: {
                y: {
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    };

    const ticketVolumeChart = new Chart(
        document.getElementById('ticketVolumeChart'),
        config
    );

}

function plotOpenChart() {
    // Plots the tickets by status doughnut chart
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
        data: data,
        options: {
            cutout: 70
        }
    };

    const ticketByStatusChart = new Chart(
        document.getElementById('ticketByStatusChart'),
        config
    );

}

function plotUserChart() {
    // Plots the tickets by assignee horizontal stacked bar chart
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
        options: {
            indexAxis: 'y',
            plugins: {
                barRoundness: 10,
            },
            barThickness: 15,
            scales: {
                y: {
                    stacked: true
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

function setTicketStatValues() {
    // Replaces the default 0s on the dashboard stats for today, month, YTD, and open tickets.
    $ticketsToday.text(ticketsToday);
    $ticketsMtd.text(ticketsMonth);
    $ticketsYtd.text(ticketsYTD);
    $ticketsOpen.text(openTickets);
}
