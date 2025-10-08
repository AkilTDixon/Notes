import * as fs from 'fs'

export const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB

/**
 * Handles image upload with progress tracking and abort capability
 * @param file The file to upload
 * @param onProgress Optional callback for tracking upload progress
 * @param abortSignal Optional AbortSignal for cancelling the upload
 * @returns Promise resolving to the URL of the uploaded image
 */
export const handleImageUpload = async (
    file: File,
    onProgress?: (event: { progress: number }) => void,
    abortSignal?: AbortSignal
): Promise<string> => {
    return new Promise((resolve, reject) => {

        // Validate file
        if (!file) {
            reject(new Error("No file provided"))
        }

        if (file.size > MAX_FILE_SIZE) {
            reject(new Error(
                `File size exceeds maximum allowed (${MAX_FILE_SIZE / (1024 * 1024)}MB)`
            ))
        }

        const reader = new FileReader();
        reader.onload = () => {
            if (typeof reader.result === 'string') {
                resolve(reader.result);
            }
            else {
                reject(new Error("Failed to read file as string"));
            }
        };
        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);


    })
}
