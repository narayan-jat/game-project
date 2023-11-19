# Helper functions.

def score_board(board):
    total_match = 0
    match_won = 0
    loss_with_friend = 0 
    loss_with_computer = 0
    draw_with_computer = 0
    draw_with_friend = 0

    for record in board:
        total_match += 1
        if record.user2 == 'computer':
            if record.status == 'won':
                match_won += 1
            elif record.status == 'Draw!':
                draw_with_computer += 1
            else:
                loss_with_computer += 1
        else:
            if record.status == 'won':
                match_won += 1
            elif record.status == 'Draw!':
                draw_with_friend += 1
            else:
                loss_with_friend += 1
    return total_match, match_won, loss_with_friend, loss_with_computer, draw_with_computer, draw_with_friend
