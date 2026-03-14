import logging
import os
from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, WorkerType, cli
from livekit.plugins import openai, simli

logger = logging.getLogger("jessica-mbs")
logger.setLevel(logging.INFO)
load_dotenv(override=True)

async def entrypoint(ctx: JobContext):
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="alloy",
            instructions="""Tu es Jessica, conseillère commerciale MBS Standoffs. 
Tu parles uniquement en français.
Tu aides les clients à trouver les bons produits du catalogue MBS.
Tu es professionnelle, chaleureuse et concise.
Tu recommandes les produits avec leur référence exacte.
Tu mentionnes la livraison express quand c'est pertinent.
Pas d'emojis, pas de markdown."""
        ),
    )
    simli_avatar = simli.AvatarSession(
        simli_config=simli.SimliConfig(
            api_key=os.getenv("SIMLI_API_KEY"),
            face_id=os.getenv("SIMLI_FACE_ID"),
        ),
    )
    await simli_avatar.start(session, room=ctx.room)
    await session.start(agent=Agent(instructions=""), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))
```

**Fichier 2** — nom : `requirements.txt` :
```
livekit-agents>=0.12.0
livekit-plugins-openai>=0.12.0
livekit-plugins-simli>=0.1.0
python-dotenv
