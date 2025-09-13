class DashboardAPI {
    constructor() {
        this.baseURL = '/api/v1/dashboard-metrics/';
        this.coursePerformanceURL = '/api/v1/course-performance/';
        this.franchiseStudentCountURL = '/api/v1/franchise-student-count/';
        this.courseManagementURL = '/api/v1/course-management/';
        this.employeeListURL = '/api/v1/employee/list/';
        this.courseCategoriesURL = '/api/v1/course-categories/';
        this.recentCoursesURL = '/api/v1/recent-courses/';
        this.recentStudentsURL = '/api/v1/recent-students/';
        this.topCoursesURL = '/api/v1/top-courses/';
    }

    getAPI() {
        // Import the API instance dynamically
        return import('./api.js').then(module => module.API);
    }

    async getDashboardMetrics() {
        try {
            const API = await this.getAPI();
            const response = await API.get('dashboard-metrics/');
            return response.data;
        } catch (error) {
            console.error('Error fetching dashboard metrics:', error);
            if (error.response?.status === 401) {
                // Token is invalid, redirect to login
                window.location.href = '/login/';
                return;
            }
            // Return null data if API fails
            return {
                success: false,
                message: 'API failed',
                data: null
            };
        }
    }

    async getCoursePerformance() {
        try {
            const API = await this.getAPI();
            const response = await API.get('course-performance/');
            return response.data;
        } catch (error) {
            console.error('Error fetching course performance:', error);
            if (error.response?.status === 401) {
                // Token is invalid, redirect to login
                window.location.href = '/login/';
                return;
            }
            // Return null data if API fails
            return {
                success: false,
                message: 'API failed',
                data: null
            };
        }
    }

    async getFranchiseStudentCount() {
        try {
            const API = await this.getAPI();
            const response = await API.get('franchise-student-count/');
            return response.data;
        } catch (error) {
            console.error('Error fetching franchise student count:', error);
            // Handle authentication errors
            if (error.response?.status === 401) {
                // Token is invalid, redirect to login
                window.location.href = '/login/';
                return;
            }
            // Return null data if API fails
            return {
                success: false,
                message: 'API failed',
                data: null
            };
        }
    }

    async getCourseManagement() {
        try {
            const API = await this.getAPI();
            const response = await API.get('course-management/');
            return response.data;
        } catch (error) {
            console.error('Error fetching course management data:', error);
            // Handle authentication errors
            if (error.response?.status === 401) {
                // Token is invalid, redirect to login
                window.location.href = '/login/';
                return;
            }
            // Return null data if API fails
            return {
                success: false,
                message: 'API failed',
                data: null
            };
        }
    }

    async getEmployeeList(page = 1, pageSize = 10, search = '') {
        try {
            const API = await this.getAPI();
            const response = await API.get(`employee/list/?page=${page}&page_size=${pageSize}&search=${search}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching employee list:', error);
            // Handle authentication errors
            if (error.response?.status === 401) {
                // Token is invalid, redirect to login
                window.location.href = '/login/';
                return;
            }
            // Return null data if API fails
            return {
                success: false,
                message: 'API failed',
                data: null
            };
        }
    }

    async getCourseCategories() {
        try {
            const API = await this.getAPI();
            const response = await API.get('course-categories/');
            return response.data;
        } catch (error) {
            console.error('Error fetching course categories:', error);
            // Handle authentication errors
            if (error.response?.status === 401) {
                // Token is invalid, redirect to login
                window.location.href = '/login/';
                return;
            }
            // Return null data if API fails
            return {
                success: false,
                message: 'API failed',
                data: null
            };
        }
    }

    

}

// Dashboard UI functions
class DashboardUI {
    constructor() {
        this.api = new DashboardAPI();
        this.metricsElements = {
            totalStudents: document.querySelector('[data-metric="total-students"]'),
            totalTrainers: document.querySelector('[data-metric="total-trainers"]'),
            totalFranchises: document.querySelector('[data-metric="total-franchises"]'),
            totalCourses: document.querySelector('[data-metric="total-courses"]'),
            ongoingCourses: document.querySelector('[data-metric="ongoing-courses"]')
        };
    }

    async loadDashboardMetrics() {
        try {
            const response = await this.api.getDashboardMetrics();
            
            if (response.success && response.data) {
                this.updateKPITiles(response.data);
            } else {
                console.warn('API failed, showing dash:', response.message);
                this.showDashForAllMetrics();
            }
        } catch (error) {
            console.error('Error loading dashboard metrics:', error);
            this.showDashForAllMetrics();
        }
    }

    async loadCoursePerformance() {
        try {
            const response = await this.api.getCoursePerformance();
            
            if (response.success && response.data) {
                this.updateCourseChart(response.data);
            } else {
                console.warn('Course performance API failed:', response.message);
                this.updateCourseChartWithFallback();
            }
        } catch (error) {
            console.error('Error loading course performance:', error);
            this.updateCourseChartWithFallback();
        }
    }

    async loadFranchiseStudentCount() {
        try {
            const response = await this.api.getFranchiseStudentCount();
            
            if (response.success && response.data) {
                this.updateFranchisePieChart(response.data);
            } else {
                console.warn('Franchise student count API failed:', response.message);
                this.updateFranchisePieChartWithFallback();
            }
        } catch (error) {
            console.error('Error loading franchise student count:', error);
            this.updateFranchisePieChartWithFallback();
        }
    }

    async loadCourseManagement() {
        try {
            const response = await this.api.getCourseManagement();
            
            if (response.success && response.data) {
                this.updateCourseManagementTable(response.data);
            } else {
                console.warn('Course management API failed:', response.message);
                this.updateCourseManagementTableWithFallback();
            }
        } catch (error) {
            console.error('Error loading course management data:', error);
            this.updateCourseManagementTableWithFallback();
        }
    }

    updateKPITiles(data) {
        // Update each KPI tile with real data
        if (this.metricsElements.totalStudents) {
            this.metricsElements.totalStudents.textContent = this.formatNumber(data.total_student_enrolments);
        }
        
        if (this.metricsElements.totalTrainers) {
            this.metricsElements.totalTrainers.textContent = this.formatNumber(data.total_trainers);
        }
        
        if (this.metricsElements.totalFranchises) {
            this.metricsElements.totalFranchises.textContent = this.formatNumber(data.total_franchises);
        }
        
        if (this.metricsElements.totalCourses) {
            this.metricsElements.totalCourses.textContent = this.formatNumber(data.total_courses);
        }
        
        if (this.metricsElements.ongoingCourses) {
            this.metricsElements.ongoingCourses.textContent = this.formatNumber(data.ongoing_courses);
        }
    }

    showDashForAllMetrics() {
        // Show "-" for all metrics when API fails
        if (this.metricsElements.totalStudents) {
            this.metricsElements.totalStudents.textContent = '-';
        }
        
        if (this.metricsElements.totalTrainers) {
            this.metricsElements.totalTrainers.textContent = '-';
        }
        
        if (this.metricsElements.totalFranchises) {
            this.metricsElements.totalFranchises.textContent = '-';
        }
        
        if (this.metricsElements.totalCourses) {
            this.metricsElements.totalCourses.textContent = '-';
        }
        
        if (this.metricsElements.ongoingCourses) {
            this.metricsElements.ongoingCourses.textContent = '-';
        }
    }

    updateCourseChart(data) {
        const labels = data.map(item => item.course_name);
        const totalStudents = data.map(item => item.total_students);
        const studentsWithJobs = data.map(item => item.students_with_jobs);
        
        if (window.courseBarChart) {
            window.courseBarChart.data.labels = labels;
            window.courseBarChart.data.datasets[0].data = totalStudents;
            window.courseBarChart.data.datasets[1].data = studentsWithJobs;
            window.courseBarChart.update();
        }
    }

    updateCourseChartWithFallback() {
        // Use fallback data if API fails
        const fallbackData = [
            { course_name: 'Web Dev', total_students: 0, students_with_jobs: 0 },
            { course_name: 'Data Science', total_students: 0, students_with_jobs: 0 },
            { course_name: 'Digital Marketing', total_students: 0, students_with_jobs: 0 },
            { course_name: 'Mobile Dev', total_students: 0, students_with_jobs: 0 },
            { course_name: 'Cybersecurity', total_students: 0, students_with_jobs: 0 }
        ];
        this.updateCourseChart(fallbackData);
    }

    updateFranchisePieChart(data) {
        const labels = data.map(item => item.franchise_name);
        const values = data.map(item => item.student_count);
        
        // Update the existing pie chart if it exists
        if (window.franchisePieChart) {
            window.franchisePieChart.data.labels = labels;
            window.franchisePieChart.data.datasets[0].data = values;
            window.franchisePieChart.update();
        }
    }

    updateFranchisePieChartWithFallback() {
        // Use fallback data if API fails
        const fallbackData = [
            { franchise_name: 'Mumbai Central', student_count: 0 },
            { franchise_name: 'Delhi NCR', student_count: 0 },
            { franchise_name: 'Bangalore', student_count: 0 },
            { franchise_name: 'Chennai', student_count: 0 },
            { franchise_name: 'Hyderabad', student_count: 0 },
            { franchise_name: 'Pune', student_count: 0 }
        ];
        this.updateFranchisePieChart(fallbackData);
    }

    updateCourseManagementTable(courses) {
        const tbody = document.querySelector('table tbody');
        if (!tbody) {
            console.error('Course management table tbody not found');
            return;
        }

        // Clear existing rows
        tbody.innerHTML = '';

        if (courses.length === 0) {
            const noDataRow = document.createElement('tr');
            noDataRow.innerHTML = `
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                    No courses found
                </td>
            `;
            tbody.appendChild(noDataRow);
            return;
        }

        courses.forEach(course => {
            const row = document.createElement('tr');
            row.className = 'bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200';
            
            // Get trainer initials for avatar
            const trainerInitials = course.trainer ? this.getInitials(course.trainer.name) : '';
            const trainerName = course.trainer ? course.trainer.name : 'Not Assigned';
            const trainerAvatarColor = this.getAvatarColor(trainerName);
            
            // Get status badge class
            const statusBadgeClass = this.getStatusBadgeClass(course.completion_status);
            
            row.innerHTML = `
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    <div>
                        <div class="font-medium text-gray-900">${course.title}</div>
                        <div class="text-xs text-gray-500 mt-1">${course.category ? course.category.name : 'No Category'}</div>
                    </div>
                </th>
                <td class="px-6 py-4">
                    ${course.duration || 'Not specified'}
                </td>
                <td class="px-6 py-4">
                    <span class="${statusBadgeClass}">
                        ${course.completion_status}
                    </span>
                </td>
                <td class="px-6 py-4">
                    ${course.total_students}
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center">
                        ${course.trainer ? `
                            <div class="w-8 h-8 ${trainerAvatarColor} rounded-full flex items-center justify-center mr-3">
                                <span class="text-sm font-medium text-white">${trainerInitials}</span>
                            </div>
                        ` : ''}
                        <div class="text-sm font-medium text-gray-900">${trainerName}</div>
                    </div>
                </td>
            `;
            
            tbody.appendChild(row);
        });
    }

    updateCourseManagementTableWithFallback() {
        const tbody = document.querySelector('table tbody');
        if (!tbody) {
            console.error('Course management table tbody not found');
            return;
        }

        // Show fallback message
        tbody.innerHTML = `
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                    Unable to load course data. Please try again later.
                </td>
            </tr>
        `;
    }


    getInitials(name) {
        if (!name) return '';
        return name.split(' ').map(word => word.charAt(0)).join('').toUpperCase().substring(0, 2);
    }

    getAvatarColor(name) {
        const colors = [
            'bg-blue-100 text-blue-600',
            'bg-green-100 text-green-600',
            'bg-purple-100 text-purple-600',
            'bg-orange-100 text-orange-600',
            'bg-red-100 text-red-600',
            'bg-yellow-100 text-yellow-600',
            'bg-indigo-100 text-indigo-600',
            'bg-pink-100 text-pink-600'
        ];
        
        // Simple hash function to get consistent color for same name
        let hash = 0;
        for (let i = 0; i < name.length; i++) {
            hash = name.charCodeAt(i) + ((hash << 5) - hash);
        }
        return colors[Math.abs(hash) % colors.length];
    }

    getStatusBadgeClass(status) {
        const statusClasses = {
            'Active': 'bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full',
            'Upcoming': 'bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded-full',
            'Completed': 'bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full',
            'Inactive': 'bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded-full'
        };
        return statusClasses[status] || statusClasses['Inactive'];
    }

    formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded shadow-lg z-50';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', async function() {
    try {
        const { isAuthenticated, checkTokenValidity } = await import('./auth.js');
        
        if (!isAuthenticated()) {
            window.location.href = '/login/';
            return;
        }
        
        const isValid = await checkTokenValidity();
        if (!isValid) {
            return; // checkTokenValidity will handle redirect
        }
        
        const dashboard = new DashboardUI();
        dashboard.loadDashboardMetrics();
        dashboard.loadCoursePerformance();
        dashboard.loadFranchiseStudentCount();
        dashboard.loadCourseManagement();
    } catch (error) {
        console.error('Authentication check failed:', error);
        window.location.href = '/login/';
    }
});
