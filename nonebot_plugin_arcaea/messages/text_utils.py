from typing import Optional

from .. import schema

def songscore(s: schema.SongScore) -> str:
    return '\n'.join((
        f"曲名: {s.song_id}",
        f"难度: {s.difficulty}",
        f"Score: {s.score}",
        f"PTT: {s.rating:.2f}",
        f"大 P: {s.shiny_perfect_count}",
        f"小 P: {s.perfect_count - s.shiny_perfect_count}",
        f"count P: {s.perfect_count}",
        f"count FAR: {s.near_count}",
        f"count MISS: {s.miss_count}",
        f"Time: {s.time_played:%F %X}"
    ))
