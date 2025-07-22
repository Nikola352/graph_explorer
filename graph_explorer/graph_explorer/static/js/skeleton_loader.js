// Skeleton Loader Management
class SkeletonLoader {
  constructor() {
    this.overlay = null;
    this.isActive = false;
    this.timeoutId = null;
    this.init();
  }

  init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        this.overlay = document.getElementById('skeleton-overlay');
      });
    } else {
      this.overlay = document.getElementById('skeleton-overlay');
    }
  }

  show(timeout = 10000) {
    if (this.overlay && !this.isActive) {
      this.overlay.classList.add('active');
      this.isActive = true;
      document.body.style.overflow = 'hidden'; // Prevent scrolling
      
      // Auto-hide after timeout as fallback
      if (timeout > 0) {
        this.timeoutId = setTimeout(() => {
          this.hide();
        }, timeout);
      }
    }
  }

  hide() {
    if (this.overlay && this.isActive) {
      this.overlay.classList.remove('active');
      this.isActive = false;
      document.body.style.overflow = ''; // Restore scrolling
      
      // Clear timeout if it exists
      if (this.timeoutId) {
        clearTimeout(this.timeoutId);
        this.timeoutId = null;
      }
    }
  }

  isVisible() {
    return this.isActive;
  }
}

// Create global instance
window.skeletonLoader = new SkeletonLoader();

// Utility functions for easy access
function showSkeleton() {
  window.skeletonLoader.show();
}

function hideSkeleton() {
  window.skeletonLoader.hide();
}

// Auto-hide skeleton on page load if it's showing
document.addEventListener('DOMContentLoaded', function() {
  // Small delay to ensure all content is loaded
  setTimeout(() => {
    if (window.skeletonLoader.isVisible()) {
      window.skeletonLoader.hide();
    }
  }, 500);
});

// Show skeleton during page transitions
window.addEventListener('beforeunload', function() {
  showSkeleton();
}); 