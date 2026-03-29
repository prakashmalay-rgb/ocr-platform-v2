import { ApiClient } from "./client";

export interface PresignedUrlResponse {
  upload_id: number;
  file_key: string;
  presigned_url: string;
}

export class UploadsService extends ApiClient {
  static async getPresignedUrl(filename: string, contentType: string): Promise<PresignedUrlResponse> {
    return this.request<PresignedUrlResponse>("/uploads/presigned-url", {
      method: "POST",
      body: JSON.stringify({ filename, content_type: contentType }),
    });
  }

  static async confirmUpload(upload_id: number, is_success: boolean): Promise<{ message: string }> {
    return this.request("/uploads/confirm", {
      method: "POST",
      body: JSON.stringify({ upload_id, is_success }),
    });
  }

  static async uploadToS3(url: string, file: File): Promise<void> {
    const response = await fetch(url, {
      method: "PUT",
      body: file,
      headers: {
        "Content-Type": file.type,
      },
    });

    if (!response.ok) {
      throw new Error("S3 Upload failed");
    }
  }
}
