// Text Analysis & Writing Assistant - Main JavaScript File

class TextAnalysisApp {
    constructor() {
        this.analysisTimeout = null;
        this.currentAnalysis = null;
        this.maxWords = 340;
        this.improvedTextVisible = false;
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        // Text input and basic stats
        this.textInput = document.getElementById('textInput');
        this.wordCountDetail = document.getElementById('wordCountDetail');
        this.charCount = document.getElementById('charCount');
        this.sentenceCount = document.getElementById('sentenceCount');
        this.paragraphCount = document.getElementById('paragraphCount');
        this.loadingOverlay = document.getElementById('loadingOverlay');

        // Analysis elements
        this.fleschScore = document.getElementById('fleschScore');
        this.gradeLevel = document.getElementById('gradeLevel');
        this.readabilityLevel = document.getElementById('readabilityLevel');
        this.overallTone = document.getElementById('overallTone');
        this.academicLevel = document.getElementById('academicLevel');
        this.wordCloud = document.getElementById('wordCloud');
        this.grammarIssues = document.getElementById('grammarIssues');
        this.styleIssues = document.getElementById('styleIssues');
        this.notificationContainer = document.getElementById('notificationContainer');

        // Action buttons
        this.fixBtn = document.getElementById('fixBtn');
        this.improveBtn = document.getElementById('improveBtn');

        // Improved text elements
        this.improvedTextSection = document.getElementById('improvedTextSection');
        this.improvedText = document.getElementById('improvedText');
        this.improvedTextTitle = document.getElementById('improvedTextTitle');
        this.improvementSummary = document.getElementById('improvementSummary');
        this.improvementType = document.getElementById('improvementType');
        this.copyImproved = document.getElementById('copyImproved');
        this.replaceOriginal = document.getElementById('replaceOriginal');
    }

    bindEvents() {
        // Text input events
        this.textInput.addEventListener('input', () => {
            this.handleTextInput();
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchTab(btn);
            });
        });

        // Clear text button
        document.getElementById('clearText').addEventListener('click', () => {
            this.clearText();
        });

        // Fix button - grammar and spelling only
        this.fixBtn.addEventListener('click', () => {
            this.fixText();
        });

        // Improve button - paraphrasing and style enhancement
        this.improveBtn.addEventListener('click', () => {
            this.improveText();
        });

        // Improved text buttons
        this.copyImproved.addEventListener('click', () => {
            this.copyImprovedText();
        });

        this.replaceOriginal.addEventListener('click', () => {
            this.replaceWithImproved();
        });

        // Click to dismiss notifications
        document.addEventListener('click', (e) => {
            if (e.target.closest('.notification')) {
                e.target.closest('.notification').remove();
            }
        });
    }

    switchTab(btn) {
        const tab = btn.dataset.tab;
        
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('tab-active'));
        btn.classList.add('tab-active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));
        document.getElementById(`tab-${tab}`).classList.remove('hidden');
    }

    handleTextInput() {
        this.updateBasicStats();
        this.checkWordLimit();
        
        // Hide improved text section when original text changes
        if (this.improvedTextVisible) {
            this.hideImprovedText();
        }
        
        // Debounce analysis
        clearTimeout(this.analysisTimeout);
        this.analysisTimeout = setTimeout(() => {
            this.analyzeText();
        }, 1000);
    }

    updateBasicStats() {
        const text = this.textInput.value;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const chars = text.length;
        const sentences = text.trim() ? text.split(/[.!?]+/).filter(s => s.trim()).length : 0;
        const paragraphs = text.trim() ? text.split(/\n\s*\n/).filter(p => p.trim()).length : 0;
        
        this.wordCountDetail.textContent = words;
        this.charCount.textContent = chars;
        this.sentenceCount.textContent = sentences;
        this.paragraphCount.textContent = paragraphs;
    }

    checkWordLimit() {
        const text = this.textInput.value.trim();
        const words = text ? text.split(/\s+/).length : 0;
        
        if (words > this.maxWords) {
            this.showNotification(`Text exceeds ${this.maxWords} words (${words} words). Consider shortening for better analysis.`, 'warning', 5000);
        }
    }

    clearText() {
        this.textInput.value = '';
        this.updateBasicStats();
        this.clearAnalysis();
        this.hideImprovedText();
        this.showNotification('Text cleared successfully!', 'success');
    }

    async fixText() {
        const text = this.textInput.value.trim();
        
        if (!text) {
            this.showNotification('Please enter some text first.', 'warning');
            return;
        }
        
        this.showLoading();
        this.fixBtn.disabled = true;
        this.fixBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Fixing...';
        
        try {
            const response = await fetch('/fix', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const result = await response.json();
            
            if (result.fixed_text && result.fixed_text !== text) {
                this.showFixedText(result.fixed_text, result.suggestions || []);
                this.showNotification('Grammar and spelling fixed!', 'success');
            } else {
                this.showNotification('No grammar issues found. Your text looks good!', 'info');
            }
        } catch (error) {
            console.error('Fix error:', error);
            this.showNotification('Error fixing text. Please try again.', 'error');
        } finally {
            this.hideLoading();
            this.fixBtn.disabled = false;
            this.fixBtn.innerHTML = '<i class="fas fa-spell-check mr-2"></i> Fix Grammar';
        }
    }

    async improveText() {
        const text = this.textInput.value.trim();
        
        if (!text) {
            this.showNotification('Please enter some text first.', 'warning');
            return;
        }
        
        this.showLoading();
        this.improveBtn.disabled = true;
        this.improveBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Improving...';
        
        try {
            const response = await fetch('/improve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const result = await response.json();
            
            if (result.improved_text && result.improved_text !== text) {
                this.showImprovedText(result.improved_text, result.suggestions || []);
                this.showNotification('Text style improved!', 'success');
            } else {
                this.showNotification('Your text style is already excellent!', 'info');
            }
        } catch (error) {
            console.error('Improve error:', error);
            this.showNotification('Error improving text. Please try again.', 'error');
        } finally {
            this.hideLoading();
            this.improveBtn.disabled = false;
            this.improveBtn.innerHTML = '<i class="fas fa-magic mr-2"></i> Improve Style';
        }
    }

    showFixedText(fixedText, suggestions) {
        this.improvedText.textContent = fixedText;
        this.improvedTextSection.style.display = 'block';
        this.improvedTextVisible = true;

        // Update title and type
        this.improvedTextTitle.textContent = 'Fixed Text';
        this.improvementType.textContent = 'Grammar Fixes';

        // Show improvement summary
        const originalLength = this.textInput.value.length;
        const fixedLength = fixedText.length;
        const changePercent = Math.round(((fixedLength - originalLength) / originalLength) * 100);
        
        let summaryHtml = `
            <div class="flex flex-wrap gap-4 text-xs">
                <span><i class="fas fa-spell-check mr-1"></i> Grammar corrected</span>
                <span><i class="fas fa-chart-line mr-1"></i> Length: ${changePercent > 0 ? '+' : ''}${changePercent}%</span>
            </div>
        `;

        if (suggestions && suggestions.length > 0) {
            summaryHtml += `<div class="mt-2 text-xs"><strong>Applied:</strong> ${suggestions.join(', ')}</div>`;
        }

        this.improvementSummary.innerHTML = summaryHtml;

        // Scroll to fixed text
        this.improvedTextSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    showImprovedText(improvedText, suggestions) {
        this.improvedText.textContent = improvedText;
        this.improvedTextSection.style.display = 'block';
        this.improvedTextVisible = true;

        // Update title and type
        this.improvedTextTitle.textContent = 'Improved Text';
        this.improvementType.textContent = 'Style Improvements';

        // Show improvement summary
        const originalLength = this.textInput.value.length;
        const improvedLength = improvedText.length;
        const changePercent = Math.round(((improvedLength - originalLength) / originalLength) * 100);
        
        let summaryHtml = `
            <div class="flex flex-wrap gap-4 text-xs">
                <span><i class="fas fa-magic mr-1"></i> Style enhanced</span>
                <span><i class="fas fa-eye mr-1"></i> Readability improved</span>
                <span><i class="fas fa-chart-line mr-1"></i> Length: ${changePercent > 0 ? '+' : ''}${changePercent}%</span>
            </div>
        `;

        if (suggestions && suggestions.length > 0) {
            summaryHtml += `<div class="mt-2 text-xs"><strong>Applied:</strong> ${suggestions.join(', ')}</div>`;
        }

        this.improvementSummary.innerHTML = summaryHtml;

        // Scroll to improved text
        this.improvedTextSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    copyImprovedText() {
        const textToCopy = this.improvedText.textContent;
        
        if (!textToCopy) {
            this.showNotification('No improved text to copy!', 'warning');
            return;
        }

        navigator.clipboard.writeText(textToCopy).then(() => {
            this.showNotification('Improved text copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Copy failed:', err);
            this.showNotification('Failed to copy text. Please try manually selecting and copying.', 'error');
        });
    }

    replaceWithImproved() {
        const improvedText = this.improvedText.textContent;
        
        if (!improvedText) {
            this.showNotification('No improved text to replace with!', 'warning');
            return;
        }

        this.textInput.value = improvedText;
        this.updateBasicStats();
        this.hideImprovedText();
        
        // Trigger analysis on the new text
        this.analyzeText();
        
        this.showNotification('Original text replaced with improved version!', 'success');
    }

    hideImprovedText() {
        this.improvedTextSection.style.display = 'none';
        this.improvedTextVisible = false;
    }

    async analyzeText() {
        const text = this.textInput.value.trim();
        
        if (!text) {
            this.clearAnalysis();
            return;
        }

        this.showLoading();
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            const analysis = await response.json();
            this.currentAnalysis = analysis;
            
            if (analysis.error) {
                this.showNotification(`Analysis error: ${analysis.error}`, 'error');
                return;
            }
            
            this.displayAnalysis(analysis);
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification('Failed to analyze text. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayAnalysis(analysis) {
        // Readability Analysis
        if (analysis.readability) {
            this.fleschScore.textContent = analysis.readability.flesch_score || 'N/A';
            this.gradeLevel.textContent = analysis.readability.grade_level || 'N/A';
            this.readabilityLevel.textContent = analysis.readability.readability_level || 'N/A';
        }

        // Sentiment Analysis
        if (analysis.sentiment) {
            this.overallTone.textContent = analysis.sentiment.overall_tone || 'N/A';
            this.academicLevel.textContent = analysis.sentiment.academic_level || 'N/A';
        }

        // Top Words
        if (analysis.top_words && analysis.top_words.length > 0) {
            const wordCloudHtml = analysis.top_words
                .slice(0, 15)
                .map(([word, count]) => `<span class="word-tag">${word} (${count})</span>`)
                .join(' ');
            this.wordCloud.innerHTML = wordCloudHtml;
        }

        // Grammar Issues
        if (analysis.grammar) {
            const grammarHtml = this.formatIssues(analysis.grammar.issues || [], 'grammar');
            this.grammarIssues.innerHTML = grammarHtml;
        }

        // Style Issues
        if (analysis.grammar) {
            const styleHtml = this.formatIssues(analysis.grammar.style_suggestions || [], 'style');
            this.styleIssues.innerHTML = styleHtml;
        }
    }

    formatIssues(issues, type) {
        if (!issues || issues.length === 0) {
            return `<div class="text-green-600 text-sm"><i class="fas fa-check-circle mr-2"></i>No ${type} issues found!</div>`;
        }

        return issues
            .slice(0, 5) // Show max 5 issues
            .map(issue => `
                <div class="issue-item">
                    <i class="fas fa-exclamation-triangle mr-2 text-yellow-500"></i>
                    <span class="text-sm">${issue.message || issue}</span>
                </div>
            `).join('');
    }

    clearAnalysis() {
        // Reset all analysis displays
        this.fleschScore.textContent = '--';
        this.gradeLevel.textContent = '--';
        this.readabilityLevel.textContent = '--';
        this.overallTone.textContent = '--';
        this.academicLevel.textContent = '--';
        this.wordCloud.innerHTML = '<span class="text-gray-500">Enter text to see word frequency</span>';
        this.grammarIssues.innerHTML = '<span class="text-gray-500">Grammar analysis will appear here</span>';
        this.styleIssues.innerHTML = '<span class="text-gray-500">Style suggestions will appear here</span>';
        
        this.currentAnalysis = null;
    }

    showLoading() {
        if (this.loadingOverlay) {
            this.loadingOverlay.style.display = 'flex';
        }
    }

    hideLoading() {
        if (this.loadingOverlay) {
            this.loadingOverlay.style.display = 'none';
        }
    }

    showNotification(message, type = 'info', duration = 3000) {
        if (!this.notificationContainer) return;

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        notification.innerHTML = `
            <i class="${icons[type] || icons.info} mr-2"></i>
            <span>${message}</span>
            <button class="ml-auto" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;

        this.notificationContainer.appendChild(notification);

        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, duration);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.textApp = new TextAnalysisApp();
});
