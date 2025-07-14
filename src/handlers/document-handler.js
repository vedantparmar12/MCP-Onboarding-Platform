import { Context } from 'hono';

export const handleDocumentUpload = async (c: Context) => {
    const method = c.req.method;
    
    if (method === 'POST') {
        try {
            const formData = await c.req.formData();
            const file = formData.get('file');
            
            if (!file) {
                return c.json({ error: 'No file provided' }, 400);
            }
            
            // Store in R2 bucket
            const key = `uploads/${Date.now()}-${file.name}`;
            await c.env.DOCUMENTS.put(key, file);
            
            return c.json({
                status: 'success',
                message: 'Document uploaded successfully',
                document_id: key,
                filename: file.name,
                size: file.size,
                timestamp: new Date().toISOString()
            });
            
        } catch (error) {
            console.error('Document upload error:', error);
            return c.json({ error: 'Upload failed' }, 500);
        }
    }
    
    if (method === 'GET') {
        try {
            const documentId = c.req.param('id');
            
            if (!documentId) {
                return c.json({ error: 'Document ID required' }, 400);
            }
            
            const object = await c.env.DOCUMENTS.get(documentId);
            
            if (!object) {
                return c.json({ error: 'Document not found' }, 404);
            }
            
            return new Response(object.body, {
                headers: {
                    'Content-Type': object.httpMetadata.contentType || 'application/octet-stream',
                    'Content-Length': object.size.toString()
                }
            });
            
        } catch (error) {
            console.error('Document retrieval error:', error);
            return c.json({ error: 'Retrieval failed' }, 500);
        }
    }
    
    return c.json({ error: 'Method not allowed' }, 405);
};
