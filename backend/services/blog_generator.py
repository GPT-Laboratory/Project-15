import os
from typing import List, Dict, Any, TypedDict
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from datetime import datetime

# Define our data models
class BlogSection(BaseModel):
    heading: str = Field(description="The section heading")
    content: str = Field(description="The section content, at least 2 paragraphs")

class BlogPost(BaseModel):
    title: str = Field(description="The title of the blog post")
    subtitle: str = Field(description="A catchy subtitle for the blog post")
    introduction: str = Field(description="An engaging introduction to the blog post, at least 2 paragraphs")
    sections: List[BlogSection] = Field(description="The main sections of the blog post, at least 3 sections")
    conclusion: str = Field(description="A thoughtful conclusion summarizing the key points, at least 1 paragraph")
    metadata: Dict[str, Any] = Field(description="Metadata about the blog post")

class GraphState(TypedDict):
    transcript: str
    video_url: str
    summary: str
    outline: List[str]
    blog_post: BlogPost
    
# Initialize LLM
def get_llm():
    """Initialize the LLM with appropriate settings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return ChatOpenAI(
        model="gpt-4-turbo",
        temperature=0.7,
        api_key=api_key
    )

# Define the graph nodes
def summarize_transcript(state: GraphState) -> GraphState:
    """Summarize the transcript to extract key points."""
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_template(
        """You are an expert content creator.
        Summarize the following transcript from a YouTube video.
        Focus on the main topics, key points, and insights.
        Keep your summary to 3-5 paragraphs.
        
        Transcript:
        {transcript}
        
        Summary:"""
    )
    
    chain = prompt | llm
    summary = chain.invoke({"transcript": state["transcript"]})
    
    state["summary"] = summary.content
    return state

def create_outline(state: GraphState) -> GraphState:
    """Create an outline for the blog post based on the summary."""
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_template(
        """You are an expert content strategist.
        Based on the following summary of a YouTube video, create an outline for a blog post.
        The outline should include a title and 3-7 main sections with headings.
        
        Summary:
        {summary}
        
        Video URL:
        {video_url}
        
        Outline:"""
    )
    
    chain = prompt | llm
    outline_response = chain.invoke({
        "summary": state["summary"],
        "video_url": state["video_url"]
    })
    
    # Extract the outline and format it as a list
    outline_text = outline_response.content
    lines = outline_text.strip().split("\n")
    
    # Process the lines to get a clean list of outline items
    outline = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("Title:") and not line.startswith("Outline:"):
            # Remove bullets, numbers, etc.
            cleaned_line = line
            for prefix in ["- ", "• ", "* ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. "]:
                if cleaned_line.startswith(prefix):
                    cleaned_line = cleaned_line[len(prefix):]
            if cleaned_line:
                outline.append(cleaned_line)
    
    state["outline"] = outline
    return state

def generate_full_blog(state: GraphState) -> GraphState:
    """Generate the full blog post using the outline and summary."""
    llm = get_llm()
    parser = PydanticOutputParser(pydantic_object=BlogPost)
    
    prompt = ChatPromptTemplate.from_template(
        """You are a professional blog writer.
        Write a comprehensive blog post based on the following outline and summary from a YouTube video.
        Make the blog post engaging, informative, and well-structured.
        Include relevant examples and actionable advice.
        Each section should have at least 2 paragraphs of content.
        
        Summary:
        {summary}
        
        Outline:
        {outline}
        
        Video Source:
        {video_url}
        
        The blog post should be formatted as a JSON object with the following structure:
        {format_instructions}
        """
    )
    
    chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser
    
    outline_text = "\n".join([f"- {item}" for item in state["outline"]])
    
    blog_post = chain.invoke({
        "summary": state["summary"],
        "outline": outline_text,
        "video_url": state["video_url"]
    })
    
    # Add metadata
    blog_post.metadata = {
        "source_video_url": state["video_url"],
        "generated_date": datetime.now().isoformat(),
        "word_count": sum(len(content.split()) for content in [
            blog_post.introduction, 
            blog_post.conclusion, 
            *[section.content for section in blog_post.sections]
        ])
    }
    
    state["blog_post"] = blog_post
    return state

def format_blog_post(state: GraphState) -> GraphState:
    """Format the blog post as Markdown."""
    blog_post = state["blog_post"]
    
    markdown = f"""# {blog_post.title}

## {blog_post.subtitle}

{blog_post.introduction}

"""
    
    for section in blog_post.sections:
        markdown += f"## {section.heading}\n\n{section.content}\n\n"
    
    markdown += f"## Conclusion\n\n{blog_post.conclusion}\n\n"
    
    markdown += f"""---

*This blog post was generated from the YouTube video: [{blog_post.title}]({state["video_url"]})*

*Generated on: {blog_post.metadata["generated_date"].split("T")[0]}*
"""
    
    # Replace the BlogPost object with the formatted markdown
    state["blog_post"] = markdown
    return state

# Create the graph
def create_processing_graph():
    """Create the LangGraph workflow for blog generation."""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("summarize_transcript", summarize_transcript)
    workflow.add_node("create_outline", create_outline)
    workflow.add_node("generate_full_blog", generate_full_blog)
    workflow.add_node("format_blog_post", format_blog_post)
    
    # Define edges
    workflow.add_edge("summarize_transcript", "create_outline")
    workflow.add_edge("create_outline", "generate_full_blog")
    workflow.add_edge("generate_full_blog", "format_blog_post")
    workflow.add_edge("format_blog_post", END)
    
    # Set the entry point
    workflow.set_entry_point("summarize_transcript")
    
    return workflow.compile()

def generate_blog_post(transcript, video_url):
    """
    Generate a blog post from a video transcript using LangChain and LangGraph.
    
    Args:
        transcript (str): The video transcript
        video_url (str): The YouTube video URL
        
    Returns:
        str: The generated blog post as markdown
    """
    # Initialize the state
    initial_state = {
        "transcript": transcript,
        "video_url": video_url,
        "summary": "",
        "outline": [],
        "blog_post": None
    }
    
    # Create and run the graph
    graph = create_processing_graph()
    final_state = graph.invoke(initial_state)
    
    return final_state["blog_post"] 