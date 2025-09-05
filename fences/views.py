from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import LocationCheckSerializer
from .models import GeoFence, DeviceState
from .utils import haversine_distance, publish_geo_event


class LocationCheckView(GenericAPIView):
    serializer_class = LocationCheckSerializer

    @swagger_auto_schema(
        request_body=LocationCheckSerializer,
        responses={200: "Check result"}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_id = serializer.validated_data["device_id"]
        lat = serializer.validated_data["lat"]
        lon = serializer.validated_data["lon"]

        fences = GeoFence.objects.all()
        inside_fences = []

        nearest = None
        for fence in fences:
            dist = haversine_distance(lat, lon, fence.center_lat, fence.center_lon)
            if dist <= fence.radius_km:
                inside_fences.append(fence)
                nearest = fence

        status = "inside" if inside_fences else "outside"

        device_state, _ = DeviceState.objects.get_or_create(device_id=device_id)
        last_state = device_state.is_inside

        if last_state != status:
            device_state.is_inside = status
            device_state.save()

            event_type = "enter" if status == "inside" else "exit"
            publish_geo_event(
                device_id=device_id,
                fence=nearest.name if nearest else None,
                event=event_type,
                lat=lat,
                lon=lon,
            )

        return Response({
            "device_id": device_id,
            "status": status,
            "fences": [{"fence": f.name} for f in inside_fences]
        })
