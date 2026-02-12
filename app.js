// Defect Management Application
class DefectManager {
    constructor() {
        this.defects = this.loadDefects();
        this.editingId = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.renderDefects();
    }

    setupEventListeners() {
        // Form submission
        document.getElementById('defect-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveDefect();
        });

        // Cancel button
        document.getElementById('cancel-btn').addEventListener('click', () => {
            this.resetForm();
        });

        // Filter controls
        document.getElementById('search-input').addEventListener('input', () => {
            this.renderDefects();
        });

        document.getElementById('filter-status').addEventListener('change', () => {
            this.renderDefects();
        });

        document.getElementById('filter-severity').addEventListener('change', () => {
            this.renderDefects();
        });

        document.getElementById('filter-priority').addEventListener('change', () => {
            this.renderDefects();
        });

        document.getElementById('clear-filters').addEventListener('click', () => {
            this.clearFilters();
        });
    }

    loadDefects() {
        const stored = localStorage.getItem('defects');
        return stored ? JSON.parse(stored) : [];
    }

    saveToStorage() {
        localStorage.setItem('defects', JSON.stringify(this.defects));
    }

    saveDefect() {
        const defect = {
            id: this.editingId || Date.now().toString(),
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            severity: document.getElementById('severity').value,
            priority: document.getElementById('priority').value,
            status: document.getElementById('status').value,
            owner: document.getElementById('owner').value,
            createdAt: this.editingId ? 
                this.defects.find(d => d.id === this.editingId).createdAt : 
                new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };

        if (this.editingId) {
            const index = this.defects.findIndex(d => d.id === this.editingId);
            this.defects[index] = defect;
        } else {
            this.defects.push(defect);
        }

        this.saveToStorage();
        this.resetForm();
        this.renderDefects();
    }

    editDefect(id) {
        const defect = this.defects.find(d => d.id === id);
        if (!defect) return;

        this.editingId = id;
        document.getElementById('defect-id').value = id;
        document.getElementById('title').value = defect.title;
        document.getElementById('description').value = defect.description;
        document.getElementById('severity').value = defect.severity;
        document.getElementById('priority').value = defect.priority;
        document.getElementById('status').value = defect.status;
        document.getElementById('owner').value = defect.owner;

        document.getElementById('form-title').textContent = 'Edit Defect';
        document.getElementById('submit-btn').textContent = 'Update Defect';
        document.getElementById('cancel-btn').style.display = 'inline-block';

        // Scroll to form
        document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
    }

    deleteDefect(id) {
        if (!confirm('Are you sure you want to delete this defect?')) return;

        this.defects = this.defects.filter(d => d.id !== id);
        this.saveToStorage();
        this.renderDefects();
    }

    resetForm() {
        this.editingId = null;
        document.getElementById('defect-form').reset();
        document.getElementById('defect-id').value = '';
        document.getElementById('form-title').textContent = 'Create New Defect';
        document.getElementById('submit-btn').textContent = 'Create Defect';
        document.getElementById('cancel-btn').style.display = 'none';
    }

    clearFilters() {
        document.getElementById('search-input').value = '';
        document.getElementById('filter-status').value = '';
        document.getElementById('filter-severity').value = '';
        document.getElementById('filter-priority').value = '';
        this.renderDefects();
    }

    getFilteredDefects() {
        let filtered = [...this.defects];

        // Search filter
        const searchTerm = document.getElementById('search-input').value.toLowerCase();
        if (searchTerm) {
            filtered = filtered.filter(d => 
                d.title.toLowerCase().includes(searchTerm) ||
                d.description.toLowerCase().includes(searchTerm)
            );
        }

        // Status filter
        const statusFilter = document.getElementById('filter-status').value;
        if (statusFilter) {
            filtered = filtered.filter(d => d.status === statusFilter);
        }

        // Severity filter
        const severityFilter = document.getElementById('filter-severity').value;
        if (severityFilter) {
            filtered = filtered.filter(d => d.severity === severityFilter);
        }

        // Priority filter
        const priorityFilter = document.getElementById('filter-priority').value;
        if (priorityFilter) {
            filtered = filtered.filter(d => d.priority === priorityFilter);
        }

        return filtered;
    }

    renderDefects() {
        const defectsList = document.getElementById('defects-list');
        const filteredDefects = this.getFilteredDefects();

        // Update count
        document.getElementById('defect-count').textContent = 
            `${filteredDefects.length} defect${filteredDefects.length !== 1 ? 's' : ''}`;

        if (filteredDefects.length === 0) {
            defectsList.innerHTML = '<p class="empty-state">No defects found. Try adjusting your filters or create a new defect!</p>';
            return;
        }

        // Sort by creation date (newest first)
        filteredDefects.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

        defectsList.innerHTML = filteredDefects.map(defect => this.createDefectCard(defect)).join('');

        // Attach event listeners
        filteredDefects.forEach(defect => {
            document.getElementById(`edit-${defect.id}`).addEventListener('click', () => {
                this.editDefect(defect.id);
            });
            document.getElementById(`delete-${defect.id}`).addEventListener('click', () => {
                this.deleteDefect(defect.id);
            });
        });
    }

    createDefectCard(defect) {
        const createdDate = new Date(defect.createdAt).toLocaleString();
        const updatedDate = new Date(defect.updatedAt).toLocaleString();
        const statusClass = defect.status.toLowerCase().replace(' ', '-');
        const severityClass = defect.severity.toLowerCase();
        const priorityClass = defect.priority.toLowerCase();

        return `
            <div class="defect-card">
                <div class="defect-header">
                    <h3 class="defect-title">${this.escapeHtml(defect.title)}</h3>
                    <div class="defect-actions">
                        <button class="btn btn-edit" id="edit-${defect.id}">Edit</button>
                        <button class="btn btn-danger" id="delete-${defect.id}">Delete</button>
                    </div>
                </div>
                <p class="defect-description">${this.escapeHtml(defect.description)}</p>
                <div class="defect-meta">
                    <div class="meta-item">
                        <span class="meta-label">Status</span>
                        <span class="badge badge-${statusClass}">${defect.status}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Severity</span>
                        <span class="badge badge-${severityClass}">${defect.severity}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Priority</span>
                        <span class="badge badge-${priorityClass}">${defect.priority}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Owner</span>
                        <span class="meta-value">${this.escapeHtml(defect.owner)}</span>
                    </div>
                </div>
                <div class="defect-timestamp">
                    <strong>Created:</strong> ${createdDate} | <strong>Updated:</strong> ${updatedDate}
                </div>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new DefectManager();
});
