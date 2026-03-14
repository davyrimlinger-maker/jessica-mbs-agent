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
        llm=openai.LLM(model="gpt-4o"),
        tts=openai.TTS(voice="alloy"),
        stt=openai.STT(),
    )
    simli_avatar = simli.AvatarSession(
        simli_config=simli.SimliConfig(
            api_key=os.getenv("SIMLI_API_KEY"),
            face_id=os.getenv("SIMLI_FACE_ID"),
        ),
    )
    await simli_avatar.start(session, room=ctx.room)
    await session.start(
        agent=Agent(instructions="Tu es Jessica, conseillere commerciale MBS Standoffs. Tu parles uniquement en francais. Tu aides les clients a trouver les bons produits du catalogue MBS. Tu es professionnelle, chaleureuse et concise."),
        room=ctx.room,
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))
