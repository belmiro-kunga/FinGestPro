document.addEventListener('DOMContentLoaded', () => {
    setupModalEventListeners();
});

function setupModalEventListeners() {
    // Close buttons
    const closeButtons = document.querySelectorAll('.close-modal');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal');
            if (modal) {
                closeModal(modal);
            }
        });
    });
    
    // Click outside to close
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal);
            }
        });
    });
    
    // Escape key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal.active');
            if (activeModal) {
                closeModal(activeModal);
            }
        }
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        
        // Focus first input if exists
        const firstInput = modal.querySelector('input, select, textarea');
        if (firstInput) {
            firstInput.focus();
        }
        
        // Trigger custom event
        modal.dispatchEvent(new CustomEvent('modalOpen'));
    }
}

function closeModal(modal) {
    if (typeof modal === 'string') {
        modal = document.getElementById(modal);
    }
    
    if (modal) {
        modal.classList.remove('active');
        
        // Reset form if exists
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
        }
        
        // Trigger custom event
        modal.dispatchEvent(new CustomEvent('modalClose'));
    }
}

function closeAllModals() {
    const modals = document.querySelectorAll('.modal.active');
    modals.forEach(modal => closeModal(modal));
}

// Export functions for use in other modules
window.modals = {
    open: openModal,
    close: closeModal,
    closeAll: closeAllModals
}; 