import { UploadsService } from "./uploads";
import { JobsService } from "./jobs";

export class UploadOrchestrator {
  static async executeFullFlow(file: File) {
    // 1. Get Presigned URL (Hide mechanics from UI)
    const { upload_id, presigned_url } = await UploadsService.getPresignedUrl(file.name, file.type);
    
    // 2. Direct S3 Upload
    await UploadsService.uploadToS3(presigned_url, file);
    
    // 3. Backend Confirmation
    await UploadsService.confirmUpload(upload_id, true);
    
    // 4. Job Creation
    const job = await JobsService.createJob(upload_id);
    
    return job; // Return job ID for UI to start tracking
  }
}
