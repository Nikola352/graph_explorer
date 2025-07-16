from typing import List, Tuple
from spotify_datasource.models import Artist
from spotify_datasource.utils import get_auth_token
from api.models.edge import Edge
from api.models.graph import Graph
import requests

from api.models.node import Node


def create_graph(auth_token: str, artist_name: str, max_neighbours: int, recursion_depth: int) -> Graph:
    artist, auth_token = find_artist_by_name(artist_name, auth_token)
    processed_artist = set()
    graph = Graph(directed=False, root_id=artist.id)
    process_artists(auth_token, artist, max_neighbours,
                    recursion_depth, processed_artist, graph)

    return graph


def process_artists(auth_token: str, artist: Artist, max_neighbours: int,
                    recursion_depth: int, processed_artists: set, graph: Graph):
    if recursion_depth == 0:
        return
    if artist.id in processed_artists:
        return

    processed_artists.add(artist.id)
    related_artists: List[Artist] = find_related_artists(
        artist, auth_token, max_neighbours)

    related_artists = [
        artist for artist in related_artists if artist.id not in processed_artists]

    if len(related_artists) > max_neighbours:
        related_artists = related_artists[:max_neighbours]

    for related_artist in related_artists:
        src_node = Node(artist.name, vars(artist))
        target_node = Node(related_artist.name, vars(related_artist))
        edge = Edge({"connection": "related"}, src_node, target_node)
        graph.add_edge(edge)
        process_artists(auth_token, related_artist, max_neighbours,
                        recursion_depth-1, processed_artists, graph)


def find_artist_by_name(artist_name: str, auth_token: str) -> Tuple[Artist, str]:
    try:
        response = requests.get("https://api.spotify.com/v1/search",
                                headers={
                                    "Authorization": f"Bearer {auth_token}"},
                                params={"q": artist_name, "type": "artist"})
    except Exception:
        raise Exception("Error: cannot fetch Spotify data!")

    if not response.ok:
        if response.status_code == 401 or response.status_code == 400:
            # send request to get new token
            # TODO try to save it to workspace
            new_auth_token = get_auth_token()
            print(new_auth_token)
            return find_artist_by_name(artist_name, new_auth_token)
        else:
            raise Exception("Something went wrong!",
                            response.reason, response.status_code)

    body = response.json()

    try:
        artists = body['artists']['items']
    except Exception:
        raise Exception("Invalid response format!")

    if len(artists) > 0:
        return Artist(artists[0]), auth_token
    else:
        raise Exception("Invalid query no artist found!")


def find_related_artists(artist: Artist, auth_token: str, max_neighbours: int) -> List[Artist]:
    # if len(artist.genres) <= 0:
    #     return []
    try:
        response = requests.get(url="https://api.spotify.com/v1/search",
                                headers={
                                    "Authorization": f"Bearer {auth_token}"},
                                params={"q": f"genre:{artist.genres[0] if artist.genres else 'hip hop'}",
                                        "type": "artist",
                                        "limit": max_neighbours*2
                                        })
    except Exception as e:
        raise Exception("Error: cannot fetch Spotify data!", e)

    if not response.ok:
        raise Exception("Something went wrong!",
                        response.reason, response.status_code, artist.id)

    body = response.json()

    try:
        artists = body['artists']['items']
    except Exception:
        raise Exception("Invalid response format!")

    return [Artist(artist) for artist in artists]
