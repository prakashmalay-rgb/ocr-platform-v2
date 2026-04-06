import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/request';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Strict SEO Guard for Staging Path (/v2)
  if (process.env.NEXT_PUBLIC_BASE_PATH === '/v2') {
    // Inject robots exclusion headers for all staging requests
    response.headers.set('X-Robots-Tag', 'noindex, nofollow, noarchive');
    
    // Safety check for accidental root contamination
    if (request.nextUrl.pathname === '/') {
        // Log staging access
        console.log('[Staging] Internal session initiated at /v2 root');
    }
  }

  return response;
}

export const config = {
  // Apply to all routes under /v2
  matcher: ['/:path*'],
};
