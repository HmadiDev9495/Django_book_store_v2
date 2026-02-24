import logging
import time
from django.utils import timezone
from .models import APILearningLog

logging.basicConfig(
    format='\033[94m[%(asctime)s]\033[0m \033[92m%(message)s\033[0m',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class RequestLearningMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.slow_requests = 0

    def __call__(self, request):
        start_time = time.time()
        self.request_count += 1
        request_id = self.request_count


        user = request.user if request.user.is_authenticated else None
        username = user.username if user else 'Anonymous'
        ip = self.get_client_ip(request)
        method = request.method
        path = request.path
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:200]


        logger.info(f"📥 [{request_id}] {method} {path} | User: {username} | IP: {ip}")


        response = self.get_response(request)


        duration_ms = (time.time() - start_time) * 1000
        is_slow = duration_ms > 500
        status = response.status_code

        if is_slow:
            self.slow_requests += 1


        if path.startswith('/api/'):
            try:
                APILearningLog.objects.create(
                    user=user,
                    ip_address=ip,
                    method=method,
                    url=request.build_absolute_uri(),
                    status_code=status,
                    response_time_ms=duration_ms,
                    is_slow=is_slow,
                    user_agent=user_agent,
                )
                db_status = "💾 Saved"
            except Exception as e:
                db_status = f"❌ DB Error: {str(e)[:30]}"
        else:
            db_status = "⏭️  Skipped (non-API)"


        status_icon = "✅" if 200 <= status < 300 else "⚠️" if status < 400 else "❌"
        speed_icon = "🐌" if is_slow else "⚡"

        logger.info(
            f"{status_icon} [{request_id}] {status} | {speed_icon} {duration_ms:.0f}ms | "
            f"Total: {self.request_count} | Slow: {self.slow_requests} | {db_status}"
        )


        if path.startswith('/api/'):
            response['X-Request-ID'] = str(request_id)
            response['X-Response-Time'] = f"{duration_ms:.2f}ms"
            response['X-Saved-To-DB'] = "Yes" if path.startswith('/api/') else "No"
            response['X-Learn-Django'] = "Model+Middleware together! 🎓"

            if is_slow:
                response['X-Performance-Tip'] = "Slow! Check admin panel for analysis 📊"

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')