from django.conf import settings
from livekit import api


def generate_livekit_token(identity, name, room_name, room_admin):
    return (
        api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(name)
        .with_grants(
            api.VideoGrants(
                room_admin=room_admin,
                room_join=True,
                room=room_name,
            ),
        )
        .to_jwt()
    )


async def start_video_call_recording(appointment_uid, room_name):
    req = api.RoomCompositeEgressRequest(
        room_name=room_name,
        audio_only=True,
        file_outputs=[
            api.EncodedFileOutput(
                file_type=api.EncodedFileType.OGG,
                filepath=f"livekit/{appointment_uid}.ogg",
                s3=api.S3Upload(
                    bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    region=settings.AWS_S3_REGION_NAME,
                    access_key=settings.AWS_ACCESS_KEY_ID,
                    secret=settings.AWS_SECRET_ACCESS_KEY,
                ),
            ),
        ],
    )

    lkapi = api.LiveKitAPI(settings.LIVEKIT_BASE_URL, settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
    await lkapi.egress.start_room_composite_egress(req)

    await lkapi.aclose()
