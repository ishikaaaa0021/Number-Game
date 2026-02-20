import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Guess the Number Game",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state variables
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'guesses' not in st.session_state:
    st.session_state.guesses = []
if 'game_history' not in st.session_state:
    st.session_state.game_history = pd.DataFrame(columns=['Date', 'Target', 'Attempts', 'Result'])
if 'game_started' not in st.session_state:
    st.session_state.game_started = time.time()
if 'min_range' not in st.session_state:
    st.session_state.min_range = 1
if 'max_range' not in st.session_state:
    st.session_state.max_range = 100
if 'hint_count' not in st.session_state:
    st.session_state.hint_count = 0
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""

# Custom CSS for better styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .info-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #e7f3ff;
        color: #004085;
        border: 1px solid #b8daff;
        margin: 10px 0;
    }
    .attempt-box {
        font-size: 18px;
        font-weight: bold;
        color: #0066cc;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
st.title("🎯 Guess the Number Game")
st.markdown("### Can you guess the secret number?")

# Sidebar for game settings and statistics
with st.sidebar:
    st.header("⚙️ Game Settings")
    
    # Player name input
    player_name = st.text_input("Your Name:", value=st.session_state.player_name)
    st.session_state.player_name = player_name if player_name else "Anonymous"
    
    # Difficulty settings
    difficulty = st.selectbox(
        "Select Difficulty:",
        ["Easy (1-50)", "Medium (1-100)", "Hard (1-200)", "Expert (1-500)"]
    )
    
    if difficulty == "Easy (1-50)":
        max_num = 50
    elif difficulty == "Medium (1-100)":
        max_num = 100
    elif difficulty == "Hard (1-200)":
        max_num = 200
    else:
        max_num = 500
    
    # New game button
    if st.button("🔄 New Game", use_container_width=True):
        st.session_state.target_number = random.randint(1, max_num)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.guesses = []
        st.session_state.game_started = time.time()
        st.session_state.min_range = 1
        st.session_state.max_range = max_num
        st.session_state.hint_count = 0
        st.rerun()
    
    st.markdown("---")
    
    # Statistics
    st.header("📊 Statistics")
    if not st.session_state.game_history.empty:
        total_games = len(st.session_state.game_history)
        avg_attempts = st.session_state.game_history['Attempts'].mean()
        best_score = st.session_state.game_history['Attempts'].min()
        
        st.metric("Total Games Played", total_games)
        st.metric("Average Attempts", f"{avg_attempts:.1f}")
        st.metric("Best Score", f"{best_score} attempts")
        
        # Performance by player
        if st.session_state.player_name:
            player_games = st.session_state.game_history[
                st.session_state.game_history['Player'] == st.session_state.player_name
            ]
            if not player_games.empty:
                st.markdown(f"**{st.session_state.player_name}'s Stats:**")
                st.metric("Games", len(player_games))
                st.metric("Avg Attempts", f"{player_games['Attempts'].mean():.1f}")
    else:
        st.info("Play a game to see statistics!")

# Main game area - Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 🔢 Guess a number between 1 and {st.session_state.max_range}")
    
    # Game status
    if not st.session_state.game_over:
        st.markdown(f"""
        <div class="info-box">
            📝 Attempts: {st.session_state.attempts} | 
            🔍 Range: {st.session_state.min_range} - {st.session_state.max_range} |
            💡 Hints used: {st.session_state.hint_count}
        </div>
        """, unsafe_allow_html=True)
    
    # Input and guess button
    if not st.session_state.game_over:
        guess = st.number_input(
            "Enter your guess:",
            min_value=1,
            max_value=st.session_state.max_range,
            value=None,
            placeholder="Type your guess here..."
        )
        
        col_guess, col_hint = st.columns([3, 1])
        
        with col_guess:
            if st.button("🎯 Submit Guess", use_container_width=True):
                if guess is not None:
                    st.session_state.attempts += 1
                    st.session_state.guesses.append(guess)
                    
                    if guess < st.session_state.target_number:
                        st.warning(f"📈 Too low! Try higher.")
                        if guess > st.session_state.min_range:
                            st.session_state.min_range = guess
                    elif guess > st.session_state.target_number:
                        st.warning(f"📉 Too high! Try lower.")
                        if guess < st.session_state.max_range:
                            st.session_state.max_range = guess
                    else:
                        # Correct guess!
                        time_taken = time.time() - st.session_state.game_started
                        st.session_state.game_over = True
                        
                        # Save to history
                        new_game = pd.DataFrame({
                            'Date': [datetime.now().strftime("%Y-%m-%d %H:%M")],
                            'Player': [st.session_state.player_name],
                            'Target': [st.session_state.target_number],
                            'Attempts': [st.session_state.attempts],
                            'Time': [f"{time_taken:.1f}s"],
                            'Result': ['Won']
                        })
                        st.session_state.game_history = pd.concat(
                            [st.session_state.game_history, new_game], 
                            ignore_index=True
                        )
                        
                        st.balloons()
                        st.markdown(f"""
                        <div class="success-box">
                            🎉 Congratulations! You got it! 🎉<br>
                            The number was {st.session_state.target_number}<br>
                            Attempts: {st.session_state.attempts} | Time: {time_taken:.1f}s
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Please enter a number!")
        
        with col_hint:
            if st.button("💡 Hint", use_container_width=True):
                st.session_state.hint_count += 1
                if st.session_state.hint_count == 1:
                    if st.session_state.target_number % 2 == 0:
                        st.info("The number is even!")
                    else:
                        st.info("The number is odd!")
                elif st.session_state.hint_count == 2:
                    if st.session_state.target_number > 50:
                        st.info("The number is greater than 50")
                    else:
                        st.info("The number is less than or equal to 50")
                elif st.session_state.hint_count == 3:
                    tens_digit = (st.session_state.target_number // 10) % 10
                    st.info(f"The tens digit is {tens_digit}")
                else:
                    st.info(f"The number is between {st.session_state.min_range} and {st.session_state.max_range}")
    
    else:
        st.markdown(f"""
        <div class="success-box">
            🎯 Game Over! Great job!<br>
            Click 'New Game' to play again!
        </div>
        """, unsafe_allow_html=True)

# Visualization area
with col2:
    st.markdown("### 📈 Live Visualization")
    
    if st.session_state.guesses:
        # Create DataFrame for plotting
        df_guesses = pd.DataFrame({
            'Attempt': range(1, len(st.session_state.guesses) + 1),
            'Guess': st.session_state.guesses
        })
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        
        # Plot 1: Guess progression
        ax1.plot(df_guesses['Attempt'], df_guesses['Guess'], 'bo-', linewidth=2, markersize=8)
        ax1.axhline(y=st.session_state.target_number, color='r', linestyle='--', 
                   label=f'Target: {st.session_state.target_number}', linewidth=2)
        ax1.fill_between(df_guesses['Attempt'], st.session_state.min_range, 
                         st.session_state.max_range, alpha=0.2, color='green', 
                         label='Valid Range')
        ax1.set_xlabel('Attempt Number')
        ax1.set_ylabel('Guess Value')
        ax1.set_title('Your Guessing Progress')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Guess distribution
        if len(st.session_state.guesses) > 1:
            df_guesses['Difference'] = abs(df_guesses['Guess'] - st.session_state.target_number)
            ax2.bar(df_guesses['Attempt'], df_guesses['Difference'], color='orange', alpha=0.7)
            ax2.set_xlabel('Attempt Number')
            ax2.set_ylabel('Distance from Target')
            ax2.set_title('How Close Were You?')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("Make your first guess to see visualization!")

# Game history and analytics
st.markdown("---")
st.header("📊 Game Analytics")

tab1, tab2, tab3 = st.tabs(["📜 Game History", "📈 Performance Charts", "🏆 Leaderboard"])

with tab1:
    if not st.session_state.game_history.empty:
        st.dataframe(
            st.session_state.game_history.sort_values('Date', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No games played yet. Start playing to see your history!")

with tab2:
    if not st.session_state.game_history.empty:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Attempts over time
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            history_df = st.session_state.game_history.copy()
            history_df['Game Number'] = range(1, len(history_df) + 1)
            
            ax1.plot(history_df['Game Number'], history_df['Attempts'], 
                    'go-', linewidth=2, markersize=8)
            ax1.set_xlabel('Game Number')
            ax1.set_ylabel('Attempts')
            ax1.set_title('Your Performance Over Time')
            ax1.grid(True, alpha=0.3)
            ax1.axhline(y=history_df['Attempts'].mean(), color='r', 
                       linestyle='--', label=f'Average: {history_df["Attempts"].mean():.1f}')
            ax1.legend()
            st.pyplot(fig1)
            plt.close()
        
        with col_chart2:
            # Attempts distribution
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.hist(history_df['Attempts'], bins=10, edgecolor='black', 
                    alpha=0.7, color='skyblue')
            ax2.set_xlabel('Number of Attempts')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Distribution of Attempts')
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)
            plt.close()
    else:
        st.info("Play some games to see performance charts!")

with tab3:
    if not st.session_state.game_history.empty:
        # Create leaderboard
        leaderboard = st.session_state.game_history.copy()
        leaderboard = leaderboard.nsmallest(10, 'Attempts')[['Player', 'Attempts', 'Date', 'Target']]
        leaderboard['Rank'] = range(1, len(leaderboard) + 1)
        leaderboard = leaderboard[['Rank', 'Player', 'Attempts', 'Date', 'Target']]
        
        st.dataframe(
            leaderboard,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": "🏆 Rank",
                "Player": "👤 Player",
                "Attempts": "🎯 Attempts",
                "Date": "📅 Date",
                "Target": "🔢 Target"
            }
        )
        
        # Best performance highlight
        best_game = leaderboard.iloc[0]
        st.success(f"🏆 Current Champion: **{best_game['Player']}** with {best_game['Attempts']} attempts!")
    else:
        st.info("Be the first to make it to the leaderboard!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    Made with ❤️ using Streamlit, Pandas, and Matplotlib | Happy Guessing! 🎯
</div>
""", unsafe_allow_html=True)
