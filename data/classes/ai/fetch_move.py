# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 14:46:47 2023

@author: Timot
"""
import re
from langchain.chat_models import ChatVertexAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

import os


#Authenticate credentials to use PALM 2 model
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'datanexus-397521-57a5a62691c0.json'

#Create dictionary to translate palm2 response to move on board
chess_dict = {
    "A": "0",
    "B": "1", 
    "C": "2", 
    "D": "3", 
    "E": "4", 
    "F": "5", 
    "G": "6",
    "H": "7",
    "a": "0",
    "b": "1", 
    "c": "2", 
    "d": "3", 
    "e": "4", 
    "f": "5", 
    "g": "6",
    "h": "7", 
    "8": "0",
    "7": "1", 
    "6": "2", 
    "5": "3", 
    "4": "4", 
    "3": "5", 
    "2": "6",
    "1": "7", 
    8: "0",
    7: "1", 
    6: "2", 
    5: "3", 
    4: "4", 
    3: "5", 
    2: "6",
    1: "7",
    }
x_dict = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
    }
class fetch:
    
    def fetch_move1(a,b,c,d,piece):
        global result
        global conversation
        global ai_move
        global res
        
        llm = ChatVertexAI()
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    """You are my opponent in a chess match. You aren't allowed to take my pieces.  If I move to a space where your piece is, you can no longer move that piece. Pawns can only move forward, knights in an L and bishops diagonally.
                   Example: Black pawn d7 to d6
                   Example: Black knight b8 to c6
                   Example: Black bishop f8 to a3
                    """
                ),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("White {move}:")
            ]
        )
        # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
        # Notice that `"chat_history"` aligns with the MessagesPlaceholder name.
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversation = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory
        )
        
        #def fetch_ai_move(x,y,x2,y2,piece):
        x=a
        piece = 'pawn '
        y=b
        x2 = c
        y2 = d
            
        human_start = x_dict[x] + chess_dict[y]
        human_end = x_dict[x2] + chess_dict[y2]
        print(human_start,human_end)
        global result
        #global conversation
        result = conversation ({"move":piece + human_start + " to " + human_end})
        
        
        ai_move = result.get('text')
        spl_word = ['knight ', 'queen ', 'king ', 'bishop ', 'rook ', 'pawn ', 'Knight ', 'Queen ', 'King ', 'Pawn ', 'Bishop ', 'Rook ']
        for i in range(12):
            match = re.search(spl_word[i],ai_move)
            if match:
                ai_move = ai_move[match.end():]
                break
            else:
                res = " "
                
        split = ' to '
        ai_move = ai_move.split(split)
        start_move = ai_move[0]
        end_move = ai_move[1]
        xstart = "".join(re.split("[^a-zA-Z]*",start_move))
        xstart = int(chess_dict[xstart])
        
        
        ystart = re.findall(r'\d+',start_move)
        ystart = ystart[0]
        ystart = int(chess_dict[ystart])
        
        
        xend = "".join(re.split("[^a-zA-Z]*",end_move))
        xend = int(chess_dict[xend])
       
        
        yend = re.findall(r'\d',end_move)
        yend = yend[0]
        yend = int(chess_dict[yend])
        print(ai_move)
        
        return xstart,ystart,xend,yend;
    
    
    def fetch_move2(a,b,c,d,piece):
        global x,y,x2,y2
        
        global ai_move
        global res
        global x2start
        global y2start
        global x2end
        global y2end
        x = a
        y = b
        x2 = c
        y2 = d
        human_start = x_dict[x] + chess_dict[y]
        human_end = x_dict[x2] + chess_dict[y2]
        result = conversation.predict(move = piece +  human_start + " to " + human_end)
        ai_move = result
        spl_word = ['knight ', 'queen ', 'king ', 'bishop ', 'rook ', 'pawn ', 'Knight ', 'Queen ', 'King ', 'Pawn ', 'Bishop ', 'Rook ']
        for i in range(12):
            match = re.search(spl_word[i],ai_move)
            if match:
                ai_move = ai_move[match.end():]
                break
            else:
                res = " "
                
        split = ' to '
        print(ai_move)
        ai_move = ai_move.split(split)
        start_move = ai_move[0]
        end_move = ai_move[1]
        x2start = "".join(re.split("[^a-zA-Z]*",start_move))
        x2start = int(chess_dict[x2start])
        y2start = re.findall(r'\d+',start_move)
        y2start = y2start[0]
        y2start = int(chess_dict[y2start])
        x2end = "".join(re.split("[^a-zA-Z]*",end_move))
        x2end = int(chess_dict[x2end])
        y2end = re.findall(r'\d',end_move)
        y2end = y2end[0]
        y2end = int(chess_dict[y2end])
        
        print(ai_move)
        
        return x2start,y2start,x2end,y2end

#fetch_ai_move(1, 4, 1, 3, 'pawn ')