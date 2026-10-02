"""Generic Manim mappings for Scene IR objects."""
from manim import Axes, Dot, MathTex, Text, VGroup

def render_timeline(obj):
    start,end=obj.data["start"],obj.data["end"]
    step=max(1,(end-start)//5 or 1)
    return Axes(x_range=[start,end,step],x_length=10,y_length=5)

def render_curve(axes,obj):
    points=obj.data["points"]
    lookup=dict(points)
    return axes.plot(lambda t: lookup[min(lookup,key=lambda x:abs(x-t))],x_range=[points[0][0],points[-1][0]]) if points else None

def render_particles(axes,obj):
    return VGroup(*[Dot(axes.c2p(i,v),radius=0.045) for i,v in enumerate(obj.data["values"])])

def render_label(obj):
    text=obj.data["text"]
    return MathTex(text) if any(c in text for c in "^_{}\\") else Text(text)

def render_object(axes,obj):
    if obj.kind=="curve": return render_curve(axes,obj)
    if obj.kind=="particles": return render_particles(axes,obj)
    if obj.kind=="label": return render_label(obj)
    return None
