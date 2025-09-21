<style>
@import '../app.css';
</style>
<template>
  <div class="container">
    <div class="row">
      <div class="col-lg-8 mb-4">
        <div class="card-header" style="background-color:#FF9900">
          <i class="bi bi-cloud-upload"></i> Contract Upload & Analysis
        </div>
        <div class="card">
          <div class="card-body">
            <!-- File Upload Section -->
            <div class="upload-section mb-4">
              <h5><i class="bi bi-file-earmark-arrow-up"></i> Upload Contract</h5>
              <form @submit="uploadDocument" enctype="multipart/form-data">
                <div class="form-group">
                  <label for="document">Select Document:</label>
                  <input 
                    type="file" 
                    id="document" 
                    ref="fileInput" 
                    @change="handleFileSelect" 
                    accept=".pdf,.txt,.doc,.docx" 
                    class="form-control" 
                  />
                </div>
                <div v-if="selectedFile" class="alert alert-info">
                  <i class="bi bi-file-earmark-text"></i> Selected file: {{ selectedFile.name }}
                  <br><small>Size: {{ formatFileSize(selectedFile.size) }}</small>
                </div>
                <button 
                  type="submit" 
                  class="btn btn-primary" 
                  :disabled="!selectedFile || uploading"
                >
                  <span v-if="uploading">
                    <i class="bi bi-hourglass-split"></i> Uploading...
                  </span>
                  <span v-else>
                    <i class="bi bi-cloud-upload"></i> Upload Document
                  </span>
                </button>
              </form>
              <div v-if="uploadResult" class="alert mt-3" :class="uploadResult.success ? 'alert-success' : 'alert-danger'">
                <i class="bi" :class="uploadResult.success ? 'bi-check-circle' : 'bi-exclamation-triangle'"></i>
                {{ uploadResult.message }}
              </div>
            </div>

            <!-- Text Response Panel -->
            <div class="response-section">
              <h5><i class="bi bi-chat-text"></i> Contract Analysis</h5>
              <div class="card">
                <div class="card-body">
                  <div v-if="analysisResult" class="analysis-result">
                    <div class="alert alert-info">
                      <strong><i class="bi bi-file-text"></i> Document: {{ analysisResult.filename }}</strong>
                    </div>
                    <div class="response-content">
                      <h6><i class="bi bi-lightbulb"></i> Analysis:</h6>
                      <div class="response-text" v-html="formatResponse(analysisResult.analysis)"></div>
                    </div>
                    <div v-if="analysisResult.keyPoints" class="key-points mt-3">
                      <h6><i class="bi bi-list-ul"></i> Key Points:</h6>
                      <ul class="list-group">
                        <li v-for="(point, index) in analysisResult.keyPoints" :key="index" class="list-group-item">
                          {{ point }}
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div v-else-if="!uploadResult" class="text-muted text-center py-4">
                    <i class="bi bi-file-earmark-text" style="font-size: 3rem;"></i>
                    <p>Upload a document to begin analysis</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Sidebar with sample documents -->
      <div class="col-lg-4 mb-4">
        <div class="card-header" style="background-color:#FF9900">
          <i class="bi bi-info-circle"></i> Supported Documents
        </div>
        <div class="card">
          <div class="card-body">
            <h6><i class="bi bi-file-earmark-pdf"></i> Supported Formats:</h6>
            <ul class="list-unstyled">
              <li><i class="bi bi-check-circle text-success"></i> PDF Documents</li>
              <li><i class="bi bi-check-circle text-success"></i> Text Files (.txt)</li>
              <li><i class="bi bi-check-circle text-success"></i> Word Documents (.doc, .docx)</li>
            </ul>
            
            <h6 class="mt-3"><i class="bi bi-lightbulb"></i> What you can do:</h6>
            <ul class="list-unstyled">
              <li><i class="bi bi-arrow-right text-primary"></i> Upload legal contracts</li>
              <li><i class="bi bi-arrow-right text-primary"></i> Analyze document content</li>
              <li><i class="bi bi-arrow-right text-primary"></i> Extract key information</li>
              <li><i class="bi bi-arrow-right text-primary"></i> Get AI-powered insights</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuthToken } from '../utils/auth'

export default {
  name: 'FileUploadView',
  data() {
    return {
      selectedFile: null,
      uploading: false,
      uploadResult: null,
      analysisResult: null
    }
  },
  methods: {
    handleFileSelect(event) {
      this.selectedFile = event.target.files[0]
      this.uploadResult = null
      this.analysisResult = null
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    formatResponse(text) {
      if (!text) return ''
      return text.replace(/\n/g, '<br>')
    },
    
    uploadDocument(e) {
      e.preventDefault()
      if (!this.selectedFile) {
        this.uploadResult = {
          success: false,
          message: 'Please select a file to upload'
        }
        return
      }

      this.uploading = true
      this.uploadResult = null
      this.analysisResult = null

      const formData = new FormData()
      formData.append('file', this.selectedFile)

      const config = {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': getAuthToken()
        }
      }

      this.axios.post('/upload', formData, config)
        .then(response => {
          this.uploading = false
          this.uploadResult = {
            success: true,
            message: `Document uploaded successfully: ${response.data.filename}`
          }
          
          // Simulate document analysis (in a real app, this would call another endpoint)
          this.simulateDocumentAnalysis(response.data.filename)
          
          this.selectedFile = null
          this.$refs.fileInput.value = ''
        })
        .catch(error => {
          this.uploading = false
          this.uploadResult = {
            success: false,
            message: `Upload failed: ${error.response?.data?.error || error.message}`
          }
        })
    },
    
    simulateDocumentAnalysis(filename) {
      // Simulate AI analysis of the uploaded document
      setTimeout(() => {
        this.analysisResult = {
          filename: filename,
          analysis: `This document has been successfully analyzed. The AI has processed the content and identified key legal concepts, clauses, and important information. The document appears to be a legal contract with standard terms and conditions.`,
          keyPoints: [
            'Document contains standard legal language',
            'Identified key contractual terms',
            'No obvious red flags detected',
            'Document structure is well-organized',
            'All necessary legal elements present'
          ]
        }
      }, 2000)
    }
  }
}
</script>
