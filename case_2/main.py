from Orchestrator import orchestrate


def Extract_Spotify_Data(request):
    """Triggered from a HTTP.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    output = orchestrate()
    if output is True:
        return {200: "Success"}
    return {500: output}


if __name__ == "__main__":
    Extract_Spotify_Data({})