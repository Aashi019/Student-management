/**// Dashboard JavaScript for real-time updates and charts

 * Real-time Dashboard with WebSocket Integrationclass Dashboard {

 * Jony Ive inspired smooth animations and interactions    constructor() {

 */        this.socket = io();

        this.charts = {};

// Initialize Socket.IO connection        this.init();

const socket = io();    }



// Chart.js instances    init() {

let enrollmentChart = null;        this.setupSocketListeners();

let gradeChart = null;        this.loadDashboardData();

let attendanceChart = null;        this.setupThemeToggle();

let studentsByGradeChart = null;        this.setupSidebar();

        this.initializeCharts();

// Connection status        this.startRealTimeUpdates();

socket.on('connect', () => {    }

    console.log('Connected to real-time server');

    showNotification('Connected to real-time updates', 'success');    setupSocketListeners() {

});        this.socket.on('connect', () => {

            console.log('Connected to server');

socket.on('disconnect', () => {            this.showNotification('Connected to server', 'success');

    console.log('Disconnected from server');        });

    showNotification('Connection lost. Reconnecting...', 'warning');

});        this.socket.on('disconnect', () => {

            console.log('Disconnected from server');

// Real-time event listeners            this.showNotification('Disconnected from server', 'warning');

socket.on('student_created', (data) => {        });

    console.log('Student created:', data);

    updateStudentCount(+1);        this.socket.on('student_added', (data) => {

    showNotification(`New student added: ${data.name}`, 'success');            this.showNotification(`New student added: ${data.name}`, 'success');

    refreshDashboard();            this.updateStudentStats();

});            this.refreshCharts();

        });

socket.on('student_updated', (data) => {

    console.log('Student updated:', data);        this.socket.on('student_updated', (data) => {

    showNotification(`Student updated: ${data.name}`, 'info');            this.showNotification(`Student updated: ${data.name}`, 'info');

    refreshDashboard();            this.refreshCharts();

});        });



socket.on('student_deleted', (data) => {        this.socket.on('student_deleted', (data) => {

    console.log('Student deleted:', data);            this.showNotification('Student deactivated', 'warning');

    updateStudentCount(-1);            this.updateStudentStats();

    showNotification('Student deactivated', 'info');            this.refreshCharts();

    refreshDashboard();        });

});    }



socket.on('grade_added', (data) => {    async loadDashboardData() {

    console.log('Grade added:', data);        try {

    showNotification('New grade recorded', 'success');            const response = await fetch('/api/dashboard/stats');

    refreshCharts();            const data = await response.json();

});            

            this.createEnrollmentChart(data.enrollment_trend);

socket.on('attendance_recorded', (data) => {            this.createGradeChart(data.grade_distribution);

    console.log('Attendance recorded:', data);            this.createAttendanceChart(data.attendance_trend);

    showNotification('Attendance updated', 'success');            

    refreshCharts();        } catch (error) {

});            console.error('Error loading dashboard data:', error);

            this.showNotification('Error loading dashboard data', 'danger');

// Initialize dashboard on page load        }

document.addEventListener('DOMContentLoaded', () => {    }

    console.log('Dashboard initializing...');

    initializeCharts();    createEnrollmentChart(data) {

    startAutoRefresh();        const ctx = document.getElementById('enrollmentChart');

    addSmoothScrolling();        if (!ctx) return;

    addCardAnimations();

});        if (this.charts.enrollment) {

            this.charts.enrollment.destroy();

// Initialize all charts        }

function initializeCharts() {

    // Chart.js default config        this.charts.enrollment = new Chart(ctx, {

    Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI'";            type: 'line',

    Chart.defaults.color = '#636366';            data: {

    Chart.defaults.plugins.legend.labels.usePointStyle = true;                labels: data.map(d => d.month),

    Chart.defaults.plugins.legend.labels.padding = 20;                datasets: [{

                        label: 'Total Students',

    // Load dashboard stats                    data: data.map(d => d.count),

    fetch('/api/stats/dashboard')                    borderColor: '#4f46e5',

        .then(response => response.json())                    backgroundColor: 'rgba(79, 70, 229, 0.1)',

        .then(result => {                    borderWidth: 3,

            if (result.success) {                    fill: true,

                const data = result.data;                    tension: 0.4,

                createEnrollmentChart(data.enrollment_trend);                    pointBackgroundColor: '#4f46e5',

                createGradeChart(data.grade_distribution);                    pointBorderColor: '#ffffff',

                createStudentsByGradeChart(data.students_by_grade);                    pointBorderWidth: 2,

                loadAttendanceTrend();                    pointRadius: 6

            }                }]

        })            },

        .catch(error => console.error('Error loading dashboard stats:', error));            options: {

}                responsive: true,

                maintainAspectRatio: false,

// Enrollment trend chart                plugins: {

function createEnrollmentChart(data) {                    legend: {

    const ctx = document.getElementById('enrollmentChart');                        display: false

    if (!ctx) return;                    }

                    },

    if (enrollmentChart) {                scales: {

        enrollmentChart.destroy();                    x: {

    }                        grid: {

                                display: false

    enrollmentChart = new Chart(ctx, {                        },

        type: 'line',                        ticks: {

        data: {                            color: '#64748b'

            labels: data.map(d => d.month),                        }

            datasets: [{                    },

                label: 'Total Students',                    y: {

                data: data.map(d => d.count),                        beginAtZero: true,

                borderColor: '#007AFF',                        grid: {

                backgroundColor: 'rgba(0, 122, 255, 0.1)',                            color: 'rgba(226, 232, 240, 0.5)'

                borderWidth: 3,                        },

                fill: true,                        ticks: {

                tension: 0.4,                            color: '#64748b'

                pointRadius: 4,                        }

                pointHoverRadius: 6,                    }

                pointBackgroundColor: '#007AFF',                },

                pointBorderColor: '#ffffff',                elements: {

                pointBorderWidth: 2                    point: {

            }]                        hoverRadius: 8

        },                    }

        options: {                }

            responsive: true,            }

            maintainAspectRatio: false,        });

            plugins: {    }

                legend: {

                    display: false    createGradeChart(data) {

                },        const ctx = document.getElementById('gradeChart');

                tooltip: {        if (!ctx) return;

                    backgroundColor: 'rgba(0, 0, 0, 0.8)',

                    padding: 12,        if (this.charts.grade) {

                    cornerRadius: 8,            this.charts.grade.destroy();

                    titleFont: {        }

                        size: 14,

                        weight: '600'        const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'];

                    },        

                    bodyFont: {        this.charts.grade = new Chart(ctx, {

                        size: 13            type: 'doughnut',

                    }            data: {

                }                labels: data.map(d => d.grade),

            },                datasets: [{

            scales: {                    data: data.map(d => d.count),

                y: {                    backgroundColor: colors.slice(0, data.length),

                    beginAtZero: true,                    borderWidth: 0,

                    grid: {                    cutout: '60%'

                        color: 'rgba(0, 0, 0, 0.05)',                }]

                        drawBorder: false            },

                    },            options: {

                    ticks: {                responsive: true,

                        padding: 10,                maintainAspectRatio: false,

                        font: {                plugins: {

                            size: 12                    legend: {

                        }                        position: 'bottom',

                    }                        labels: {

                },                            padding: 20,

                x: {                            usePointStyle: true,

                    grid: {                            color: '#64748b'

                        display: false                        }

                    },                    }

                    ticks: {                }

                        padding: 10,            }

                        font: {        });

                            size: 12    }

                        }

                    }    createAttendanceChart(data) {

                }        const ctx = document.getElementById('attendanceChart');

            },        if (!ctx) return;

            interaction: {

                intersect: false,        if (this.charts.attendance) {

                mode: 'index'            this.charts.attendance.destroy();

            },        }

            animation: {

                duration: 750,        this.charts.attendance = new Chart(ctx, {

                easing: 'easeInOutQuart'            type: 'bar',

            }            data: {

        }                labels: data.map(d => new Date(d.date).toLocaleDateString()),

    });                datasets: [{

}                    label: 'Attendance Rate (%)',

                    data: data.map(d => d.rate),

// Grade distribution chart                    backgroundColor: 'rgba(16, 185, 129, 0.8)',

function createGradeChart(data) {                    borderColor: '#10b981',

    const ctx = document.getElementById('gradeChart');                    borderWidth: 2,

    if (!ctx) return;                    borderRadius: 4

                    }]

    if (gradeChart) {            },

        gradeChart.destroy();            options: {

    }                responsive: true,

                    maintainAspectRatio: false,

    const grades = ['A', 'B', 'C', 'D', 'F'];                plugins: {

    const counts = grades.map(grade => {                    legend: {

        const found = data.find(d => d.grade === grade);                        display: false

        return found ? found.count : 0;                    }

    });                },

                    scales: {

    gradeChart = new Chart(ctx, {                    x: {

        type: 'doughnut',                        grid: {

        data: {                            display: false

            labels: grades,                        },

            datasets: [{                        ticks: {

                data: counts,                            color: '#64748b',

                backgroundColor: [                            maxTicksLimit: 7

                    '#34C759',  // A - Success green                        }

                    '#007AFF',  // B - Primary blue                    },

                    '#FF9500',  // C - Warning orange                    y: {

                    '#FF3B30',  // D - Danger red                        beginAtZero: true,

                    '#8E8E93'   // F - Gray                        max: 100,

                ],                        grid: {

                borderWidth: 0,                            color: 'rgba(226, 232, 240, 0.5)'

                hoverOffset: 8                        },

            }]                        ticks: {

        },                            color: '#64748b',

        options: {                            callback: function(value) {

            responsive: true,                                return value + '%';

            maintainAspectRatio: false,                            }

            plugins: {                        }

                legend: {                    }

                    position: 'right',                }

                    labels: {            }

                        padding: 15,        });

                        font: {    }

                            size: 13,

                            weight: '500'    async refreshCharts() {

                        }        await this.loadDashboardData();

                    }    }

                },

                tooltip: {    async updateStudentStats() {

                    backgroundColor: 'rgba(0, 0, 0, 0.8)',        try {

                    padding: 12,            const response = await fetch('/api/students/chart-data');

                    cornerRadius: 8            const data = await response.json();

                }            

            },            // Update student count if element exists

            animation: {            const totalStudentsEl = document.getElementById('totalStudents');

                animateRotate: true,            if (totalStudentsEl) {

                animateScale: true,                const total = data.by_grade.reduce((sum, item) => sum + item.count, 0);

                duration: 1000,                totalStudentsEl.textContent = total;

                easing: 'easeInOutQuart'                this.animateNumber(totalStudentsEl, total);

            }            }

        }            

    });        } catch (error) {

}            console.error('Error updating student stats:', error);

        }

// Students by grade level chart    }

function createStudentsByGradeChart(data) {

    const ctx = document.getElementById('studentsByGradeChart');    animateNumber(element, targetNumber) {

    if (!ctx) return;        const startNumber = parseInt(element.textContent) || 0;

            const duration = 1000;

    if (studentsByGradeChart) {        const startTime = Date.now();

        studentsByGradeChart.destroy();        

    }        const updateNumber = () => {

                const elapsed = Date.now() - startTime;

    studentsByGradeChart = new Chart(ctx, {            const progress = Math.min(elapsed / duration, 1);

        type: 'bar',            const currentNumber = Math.floor(startNumber + (targetNumber - startNumber) * progress);

        data: {            

            labels: data.map(d => d.grade),            element.textContent = currentNumber;

            datasets: [{            

                label: 'Students',            if (progress < 1) {

                data: data.map(d => d.count),                requestAnimationFrame(updateNumber);

                backgroundColor: 'rgba(0, 122, 255, 0.8)',            }

                borderRadius: 8,        };

                hoverBackgroundColor: '#007AFF'        

            }]        updateNumber();

        },    }

        options: {

            responsive: true,    setupThemeToggle() {

            maintainAspectRatio: false,        const themeToggle = document.getElementById('themeToggle');

            plugins: {        const currentTheme = localStorage.getItem('theme') || 'light';

                legend: {        

                    display: false        document.documentElement.setAttribute('data-theme', currentTheme);

                },        

                tooltip: {        if (themeToggle) {

                    backgroundColor: 'rgba(0, 0, 0, 0.8)',            themeToggle.addEventListener('click', () => {

                    padding: 12,                const currentTheme = document.documentElement.getAttribute('data-theme');

                    cornerRadius: 8                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

                }                

            },                document.documentElement.setAttribute('data-theme', newTheme);

            scales: {                localStorage.setItem('theme', newTheme);

                y: {                

                    beginAtZero: true,                const icon = themeToggle.querySelector('i');

                    grid: {                if (icon) {

                        color: 'rgba(0, 0, 0, 0.05)',                    icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';

                        drawBorder: false                }

                    },            });

                    ticks: {        }

                        padding: 10    }

                    }

                },    setupSidebar() {

                x: {        const sidebarToggle = document.getElementById('sidebarToggle');

                    grid: {        const sidebar = document.querySelector('.sidebar');

                        display: false        const overlay = document.querySelector('.sidebar-overlay');

                    },        

                    ticks: {        if (sidebarToggle && sidebar) {

                        padding: 10            sidebarToggle.addEventListener('click', () => {

                    }                sidebar.classList.toggle('active');

                }                if (overlay) {

            },                    overlay.classList.toggle('active');

            animation: {                }

                duration: 750,            });

                easing: 'easeInOutQuart'        }

            }        

        }        if (overlay) {

    });            overlay.addEventListener('click', () => {

}                sidebar.classList.remove('active');

                overlay.classList.remove('active');

// Load attendance trend            });

function loadAttendanceTrend() {        }

    fetch('/api/stats/attendance-trend?days=30')    }

        .then(response => response.json())

        .then(result => {    initializeCharts() {

            if (result.success) {        // Set Chart.js defaults

                createAttendanceChart(result.data);        Chart.defaults.font.family = 'Inter, sans-serif';

            }        Chart.defaults.color = '#64748b';

        })        Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(0, 0, 0, 0.8)';

        .catch(error => console.error('Error loading attendance trend:', error));        Chart.defaults.plugins.tooltip.titleColor = '#ffffff';

}        Chart.defaults.plugins.tooltip.bodyColor = '#ffffff';

        Chart.defaults.plugins.tooltip.borderColor = 'rgba(255, 255, 255, 0.1)';

// Attendance trend chart        Chart.defaults.plugins.tooltip.borderWidth = 1;

function createAttendanceChart(data) {        Chart.defaults.plugins.tooltip.cornerRadius = 8;

    const ctx = document.getElementById('attendanceChart');    }

    if (!ctx) return;

        startRealTimeUpdates() {

    if (attendanceChart) {        // Update charts every 5 minutes

        attendanceChart.destroy();        setInterval(() => {

    }            this.refreshCharts();

            }, 5 * 60 * 1000);

    attendanceChart = new Chart(ctx, {        

        type: 'line',        // Update stats every minute

        data: {        setInterval(() => {

            labels: data.map(d => new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),            this.updateStudentStats();

            datasets: [{        }, 60 * 1000);

                label: 'Attendance Rate (%)',    }

                data: data.map(d => d.rate),

                borderColor: '#34C759',    showNotification(message, type = 'info') {

                backgroundColor: 'rgba(52, 199, 89, 0.1)',        const notification = document.createElement('div');

                borderWidth: 3,        notification.className = `alert alert-${type} notification`;

                fill: true,        notification.innerHTML = `

                tension: 0.4,            <i class="fas fa-${this.getNotificationIcon(type)}"></i>

                pointRadius: 3,            <span>${message}</span>

                pointHoverRadius: 5,        `;

                pointBackgroundColor: '#34C759',        

                pointBorderColor: '#ffffff',        // Add to notification container or create one

                pointBorderWidth: 2        let container = document.querySelector('.notification-container');

            }]        if (!container) {

        },            container = document.createElement('div');

        options: {            container.className = 'notification-container';

            responsive: true,            container.style.cssText = `

            maintainAspectRatio: false,                position: fixed;

            plugins: {                top: 1rem;

                legend: {                right: 1rem;

                    display: false                z-index: 9999;

                },                max-width: 400px;

                tooltip: {            `;

                    backgroundColor: 'rgba(0, 0, 0, 0.8)',            document.body.appendChild(container);

                    padding: 12,        }

                    cornerRadius: 8,        

                    callbacks: {        container.appendChild(notification);

                        label: (context) => `${context.parsed.y}%`        

                    }        // Auto remove after 5 seconds

                }        setTimeout(() => {

            },            notification.remove();

            scales: {        }, 5000);

                y: {        

                    beginAtZero: true,        // Add click to dismiss

                    max: 100,        notification.addEventListener('click', () => {

                    grid: {            notification.remove();

                        color: 'rgba(0, 0, 0, 0.05)',        });

                        drawBorder: false    }

                    },

                    ticks: {    getNotificationIcon(type) {

                        callback: (value) => `${value}%`,        const icons = {

                        padding: 10            success: 'check-circle',

                    }            danger: 'exclamation-triangle',

                },            warning: 'exclamation-circle',

                x: {            info: 'info-circle'

                    grid: {        };

                        display: false        return icons[type] || 'info-circle';

                    },    }

                    ticks: {}

                        maxRotation: 45,

                        minRotation: 45,// Initialize dashboard when DOM is loaded

                        padding: 10,document.addEventListener('DOMContentLoaded', () => {

                        font: {    new Dashboard();

                            size: 11});

                        }

                    }// Utility functions

                }function formatNumber(num) {

            },    return new Intl.NumberFormat().format(num);

            animation: {}

                duration: 750,

                easing: 'easeInOutQuart'function formatPercentage(num) {

            }    return new Intl.NumberFormat('en-US', {

        }        style: 'percent',

    });        minimumFractionDigits: 1,

}        maximumFractionDigits: 1

    }).format(num / 100);

// Update student count with animation}

function updateStudentCount(delta) {

    const element = document.getElementById('totalStudents');// Export for use in other scripts

    if (element) {window.Dashboard = Dashboard;

        const currentCount = parseInt(element.textContent);
        const newCount = currentCount + delta;
        animateValue(element, currentCount, newCount, 500);
    }
}

// Animate number changes
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            element.textContent = end;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Refresh dashboard data
function refreshDashboard() {
    fetch('/api/stats/dashboard')
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const data = result.data;
                updateDashboardStats(data.overview);
                refreshCharts();
            }
        })
        .catch(error => console.error('Error refreshing dashboard:', error));
}

// Update dashboard statistics
function updateDashboardStats(stats) {
    if (stats.total_students !== undefined) {
        const elem = document.getElementById('totalStudents');
        if (elem) elem.textContent = stats.total_students;
    }
    if (stats.total_subjects !== undefined) {
        const elem = document.getElementById('totalSubjects');
        if (elem) elem.textContent = stats.total_subjects;
    }
    if (stats.attendance_rate !== undefined) {
        const elem = document.getElementById('attendanceRate');
        if (elem) elem.textContent = `${stats.attendance_rate}%`;
    }
    if (stats.average_gpa !== undefined) {
        const elem = document.getElementById('averageGPA');
        if (elem) elem.textContent = stats.average_gpa;
    }
}

// Refresh all charts
function refreshCharts() {
    initializeCharts();
}

// Auto-refresh dashboard every 30 seconds
function startAutoRefresh() {
    setInterval(() => {
        refreshDashboard();
    }, 30000);
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add smooth scrolling
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add card hover animations
function addCardAnimations() {
    const cards = document.querySelectorAll('.stat-card, .card, .chart-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Refresh individual chart
function refreshChart(chartName) {
    console.log(`Refreshing ${chartName} chart...`);
    refreshCharts();
}

// Export for use in HTML
window.refreshChart = refreshChart;
