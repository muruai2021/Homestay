/**
 * API 请求工具类
 */

class ApiClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }

    async post(endpoint, data, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response;
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    async stream(endpoint, data, onChunk, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';
        let lastRenderLen = 0;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            fullContent += chunk;

            if (fullContent.length - lastRenderLen >= CONFIG.STREAM_UPDATE_THRESHOLD || done) {
                if (onChunk) {
                    onChunk(fullContent);
                }
                lastRenderLen = fullContent.length;
            }
        }

        return fullContent;
    }
}

const api = new ApiClient(CONFIG.API_URL);
window.api = api;
