/**
 * Validates phone number format
 * Only accepts digits (0-9)
 * 
 * @param {string} phone - The phone number to validate
 * @returns {Object} - Object with isValid boolean and error message
 */
export function validatePhone(phone) {
    // If phone is empty, it's valid (optional field)
    if (!phone || phone.trim() === '') {
        return {
            isValid: true,
            errorMessage: ''
        };
    }

    // Remove all non-digit characters
    const cleanedPhone = phone.replace(/\D/g, '');
    
    // Check if it's exactly 10 digits
    if (/^\d{10}$/.test(cleanedPhone)) {
        return {
            isValid: true,
            errorMessage: ''
        };
    }
    
    return {
        isValid: false,
        errorMessage: 'Please enter exactly 10 digits for phone number'
    };
}

/**
 * Validates country code format
 * 
 * @param {string} countryCode - The country code to validate
 * @returns {Object} - Object with isValid boolean and error message
 */
export function validateCountryCode(countryCode) {
    // If country code is empty, it's valid (optional field)
    if (!countryCode || countryCode.trim() === '') {
        return {
            isValid: true,
            errorMessage: ''
        };
    }

    // Check if it starts with + and has 1-4 digits
    if (/^\+\d{1,4}$/.test(countryCode)) {
        return {
            isValid: true,
            errorMessage: ''
        };
    }
    
    return {
        isValid: false,
        errorMessage: 'Please enter a valid country code (e.g., +91, +1, +44)'
    };
}

/**
 * Shows field error message
 * 
 * @param {HTMLElement} element - The error element to show
 * @param {string} message - The error message to display
 */
export function showFieldError(element, message) {
    if (element) {
        element.classList.add('hidden');
        element.textContent = message;
        element.classList.remove('hidden');
    }
}

/**
 * Hides field error message
 * 
 * @param {HTMLElement} element - The error element to hide
 */
export function hideFieldError(element) {
    if (element) {
        element.classList.add('hidden');
        element.textContent = '';
    }
}

/**
 * Validates phone input in real-time
 * 
 * @param {HTMLInputElement} inputElement - The phone input element
 * @param {HTMLElement} errorElement - The error display element
 */
export function setupPhoneValidation(inputElement, errorElement) {
    if (!inputElement || !errorElement) {
        console.warn('Phone validation setup: Missing input or error element');
        return;
    }
    
    // Only allow digits
    inputElement.addEventListener('input', function() {
        // Remove all non-digit characters
        this.value = this.value.replace(/\D/g, '');
        
        // Limit to 10 digits
        if (this.value.length > 10) {
            this.value = this.value.substring(0, 10);
        }
        
        hideFieldError(errorElement);
    });
    
    // Validate on blur
    inputElement.addEventListener('blur', function() {
        const validation = validatePhone(this.value);
        if (!validation.isValid) {
            showFieldError(errorElement, validation.errorMessage);
        } else {
            hideFieldError(errorElement);
        }
    });
}

/**
 * Validates country code input in real-time
 * 
 * @param {HTMLInputElement} inputElement - The country code input element
 * @param {HTMLElement} errorElement - The error display element
 */
export function setupCountryCodeValidation(inputElement, errorElement) {
    if (!inputElement || !errorElement) {
        console.warn('Country code validation setup: Missing input or error element');
        return;
    }
    
    // Only allow + and digits
    inputElement.addEventListener('input', function() {
        // Remove all characters except + and digits
        this.value = this.value.replace(/[^\d+]/g, '');
        
        // Ensure it starts with +
        if (this.value && !this.value.startsWith('+')) {
            this.value = '+' + this.value;
        }
        
        // Limit to 5 characters (+ and up to 4 digits)
        if (this.value.length > 5) {
            this.value = this.value.substring(0, 5);
        }
        
        hideFieldError(errorElement);
    });
    
    // Validate on blur
    inputElement.addEventListener('blur', function() {
        const validation = validateCountryCode(this.value);
        if (!validation.isValid) {
            showFieldError(errorElement, validation.errorMessage);
        } else {
            hideFieldError(errorElement);
        }
    });
} 