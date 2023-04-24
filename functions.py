def get_item(item):
    return item.split('/')[-1].split('.')[0]



def find_result(user_r, bot_r):
    if user_r == 'Paper':
        if bot_r == 'Paper':
            return 'Draw'
        elif bot_r == 'Rock':
            return 'Win'
        elif bot_r == 'Scissors':
            return 'Lose'
    elif user_r == 'Rock':
        if bot_r == 'Paper':
            return 'Lose'
        elif bot_r == 'Rock':
            return 'Draw'
        elif bot_r == 'Scissors':
            return 'Win'
    elif user_r == 'Scissors':
        if bot_r == 'Paper':
            return 'Win'
        elif bot_r == 'Rock':
            return 'Lose'
        elif bot_r == 'Scissors':
            return 'Draw'

def update_db(db_session, current_user, User, result):
    db_sess = db_session.create_session()
    email = current_user.email

    user = db_sess.query(User).filter(User.email == email).first()

    if result == 'Win':
        user.update_stats1()
    elif result == 'Lose':
        user.update_stats3()
    elif result == 'Draw':
        user.update_stats2()
    user.update_stats5()
    db_sess.commit()