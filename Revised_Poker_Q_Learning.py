#import the appropriate modules
import random
import time
import copy

#global variables
l_deck = []
l_dealt_cards = []
player_count = 9
original_player_count = player_count
player_cards = []
community_cards = []
value = 0
l_players = []
player_type_list = ['Aggressive', 'Normal', 'Conservative']
correct_combo = []
l_value_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
l_value_order1 = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
low_values_list1 = ['A', '2', '3', '4', '5', '6']
low_values_list = ['2', '3', '4', '5', '6']
medium_values_list = ['7', '8', '9']
high_values_list = ['10', 'J', 'Q', 'K', 'A']
l_suite_order = ['D', 'C', 'H', 'S']
l_results = []
l_hand_rankings = ['Royal Flush', 'Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 'One Pair', 'High Card']
l_eliminated_players = []
dealer_order = 0
big_blind = 0
small_blind = 0
big_blind_amount = 10
original_big_blind_amount = big_blind_amount
small_blind_amount = 5
raise_amount = big_blind_amount
player_buyin_amount = 100
betting_temp_player_list = []
human_players = []
folded_players = []
pot = 0
q_tables = [{}, {}, {}, {}]

#			  Bet11							  Low Pair , Medium Pair , High Pair
l_matrices = {'decision_before_flop_pair' : [['Raise'  , 'Raise'     , 'Raise'],  #Aggressive
											 ['Call'  , 'Call'	 , 'Raise'],  #Normal
											 ['Fold'   , 'Call'	 , 'Call']], #Conservative

#			  Bet12												    5       , 4       , 3       , 2       , 1
			  'decision_before_flop_in_range_of_straight_flush' : [['Raise' , 'Raise' , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  													   ['Call' , 'Call' , 'Call' , 'Call' , 'Call'],  #Normal
			  													   ['Fold'  , 'Fold'  , 'Fold'  , 'Fold'  , 'Fold' ]], #Conservative

#			  Bet13								    10-12   , 6-9												   
			  'decision_before_flop_same_suite' : [['Raise' , 'Raise'],  #Aggressive
												   ['Call' , 'Call'],  #Normal
												   ['Fold'  , 'Call']], #Conservative

#			  Bet14										      5       , 4       , 3       , 2       , 1
			  'decision_before_flop_in_range_of_straight' : [['Raise' , 'Raise' , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  												 ['Call' , 'Call' , 'Call' , 'Raise' , 'Raise'],  #Normal
			  												 ['Fold'  , 'Fold'  , 'Call' , 'Call' , 'Call']], #Conservative

#			  Bet15										    L + M   , L + H   , M + H
			  'decision_before_flop_two_distinct_cards' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  											   ['Call' , 'Call' , 'Call'],  #Normal
			  											   ['Fold'  , 'Fold'  , 'Fold' ]], #Conservative

#			  Bet16										  Low Pair , Medium Pair , High Pair
			  'decision_before_flop_highest_bet_pair' : [['Raise'  , 'Raise'     , 'Raise'],  #Aggressive
			  											 ['Call'   , 'Call'      , 'Call' ],  #Normal
			  											 ['Fold'   , 'Fold'      , 'Call' ]], #Conservative

#			  Bet17																5       , 4       , 3       , 2       , 1
			  'decision_before_flop_highest_bet_in_range_of_straight_flush' : [['Raise' , 'Raise' , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  													   			   ['Call'  , 'Call'  , 'Call'  , 'Call'  , 'Call' ],  #Normal
			  													  			   ['Fold'  , 'Fold'  , 'Fold'  , 'Fold'  , 'Fold' ]], #Conservative

#			  Bet18												L + M   , L + H
			  'decision_before_flop_highest_bet_same_suite' : [['Raise' , 'Raise'],  #Aggressive
			  												   ['Call'  , 'Call' ],  #Normal
			  												   ['Fold'  , 'Fold' ]], #Conservative
 
#			  Bet19														  5       , 4       , 3       , 2       , 1
			  'decision_before_flop_highest_bet_in_range_of_straight' : [['Raise' , 'Raise' , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  															 ['Call'  , 'Call'  , 'Call'  , 'Call'  , 'Call' ],  #Normal
			  															 ['Fold'  , 'Fold'  , 'Call'  , 'Call'  , 'Call' ]], #Conservative

#			  Bet110												    L + M   , L + H   , M + H
			  'decision_before_flop_highest_bet_two_distinct_cards' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  														   ['Fold'  , 'Call'  , 'Call' ],  #Normal
			  														   ['Fold'  , 'Fold'  , 'Fold' ]], #Conservative

#			  Bet21									 Diamonds , Clubs   , Hearts  , Spades
			  'decision_before_turn_royal_flush' : [['Raise'  , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  										['Raise'  , 'Raise' , 'Raise' , 'Raise'],  #Normal
			  										['Check'  , 'Check' , 'Check' , 'Check']], #Conservative

#			  Bet22									    Diamonds High , Diamonds Medium , Diamonds Low , Clubs High , Clubs Medium , Clubs Low , Hearts High , Hearts Medium , Hearts Low , Spades High , Spades Medium , Spades Low
			  'decision_before_turn_straight_flush' : [['Raise'       , 'Raise'         , 'Raise'      , 'Raise' 	, 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 		, 'Raise'   ],  #Aggressive
			  										   ['Raise'       , 'Raise'         , 'Raise'      , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	    , 'Raise'   ],  #Normal
			  										   ['Check'       , 'Check'         , 'Check' 	   , 'Check'    , 'Check'      , 'Check'   , 'Check'     , 'Check'       , 'Check'    , 'Check'     , 'Check' 		, 'Check'	]], #Conservative

#			  Bet23										High    , Medium  , Low
			  'decision_before_turn_four_of_a_kind' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  										   ['Raise' , 'Raise' , 'Raise'],  #Normal
			  										   ['Check' , 'Check' , 'Check']], #Conservative

#			  Bet24 - Three of a Kind is:           High    , Medium  , Low
			  'decision_before_turn_full_house' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  									   ['Raise' , 'Raise' , 'Raise'],  #Normal
			  									   ['Check' , 'Check' , 'Check']], #Conservative

#			  Bet25 - High Card is:			   Diamonds High , Diamonds Medium , Diamonds Low , Clubs High , Clubs Medium , Clubs Low , Hearts High , Hearts Medium , Hearts Low , Spades High , Spades Medium , Spades Low
			  'decision_before_turn_flush' : [['Raise'       , 'Raise'         , 'Raise'      , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	   , 'Raise'   ],  #Aggressive
			  								  ['Check'       , 'Check'         , 'Check'      , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	   , 'Raise'   ],  #Normal
			  								  ['Check'       , 'Check'         , 'Check' 	  , 'Check'    , 'Check'      , 'Check'   , 'Check'     , 'Check'       , 'Check'    , 'Check'     , 'Check' 	   , 'Check'   ]], #Conservative

#			  Bet26								  Diamonds High , Diamonds Medium , Diamonds Low , Clubs High , Clubs Medium , Clubs Low , Hearts High , Hearts Medium , Hearts Low , Spades High , Spades Medium , Spades Low
			  'decision_before_turn_straight' : [['Raise'       , 'Raise'         , 'Raise'      , 'Raise' 	  , 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	  , 'Raise'	  ],  #Aggressive
			  									 ['Check'       , 'Check'         , 'Check'      , 'Check'    , 'Check'      , 'Check'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	  , 'Raise'	  ],  #Normal
			  									 ['Check'       , 'Check'         , 'Check' 	 , 'Check'    , 'Check'      , 'Check'   , 'Check'     , 'Check'       , 'Check'    , 'Check'     , 'Check'    	  , 'Check'	  ]], #Conservative

#			  Bet27										 High    , Medium  , Low
			  'decision_before_turn_three_of_a_kind' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  											['Raise' , 'Raise' , 'Check'],  #Normal
			  											['Check' , 'Check' , 'Fold' ]], #Conservative

#			  Bet28								  High High , High Medium , High Low , Medium Medium , Medium Low , Low Low
			  'decision_before_turn_two_pair' : [['Raise'   , 'Raise'     , 'Raise'  , 'Raise'       , 'Raise'    , 'Raise' ],  #Aggressive
			  									 ['Raise'   , 'Raise'     , 'Raise'  , 'Check'       , 'Check'    , 'Check' ],  #Normal
			  									 ['Check'   , 'Check'     , 'Check'  , 'Fold'        , 'Fold'     , 'Fold'  ]], #Conservative

#			  Bet29							      High    , Medium  , Low
			  'decision_before_turn_one_pair' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  									 ['Raise' , 'Check' , 'Check'],  #Normal
			  									 ['Check' , 'Fold'  , 'Fold' ]], #Conservative

#			  Bet210 - Number of in range cards:				 3       , 4
			  'decision_before_turn_in_range_of_royal_flush' : [['Raise' , 'Raise'],  #Aggressive
			  													['Check' , 'Raise'],  #Normal
			  													['Check' , 'Check']], #Conservative

#			  Bet211												Diamonds , Clubs   , Hearts  , Spades
			  'decision_before_turn_in_range_of_straight_flush' : [['Raise'  , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  													   ['Check'  , 'Check' , 'Raise' , 'Raise'],  #Normal
			  													   ['Check'  , 'Check' , 'Check' , 'Check']], #Conservative

#			  Bet212 - Number of in range cards:									3       , 4
			  'decision_before_turn_in_range_of_royal_flush_and_straight_flush' : [['Raise' , 'Raise'],  #Aggressive
			  																	   ['Raise' , 'Raise'],  #Normal
			  																	   ['Check' , 'Check']], #Conservative

#			  Bet213									   Diamonds , Clubs   , Hearts  , Spades
			  'decision_before_turn_in_range_of_flush' : [['Raise'  , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  											  ['Check'  , 'Check' , 'Raise' , 'Raise'],  #Normal
			  											  ['Check'  , 'Check' , 'Check' , 'Check']], #Conservative   
												 
#			  Bet214										  3        , 4 
			  'decision_before_turn_in_range_of_straight' : [['Raise' , 'Raise'],  #Aggressive
			  												 ['Check' , 'Raise'],  #Normal
			  												 ['Fold'  , 'Check']], #Conservative

#			  Bet215 - Highest Card is:					    Diamonds High , Diamonds Medium , Diamonds Low , Clubs High , Clubs Medium , Clubs Low , Hearts High , Hearts Medium , Hearts Low , Spades High , Spades Medium , Spades Low
			  'decision_before_turn_all_distinct_cards' : [['Raise'       , 'Raise'         , 'Raise'      , 'Raise' 	, 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	    , 'Raise'	],  #Aggressive
			  										   	   ['Check'       , 'Check'         , 'Check'      , 'Check'    , 'Check'      , 'Check'   , 'Check'     , 'Check'       , 'Check'    , 'Check'     , 'Check' 	    , 'Check'	],  #Normal
			  										   	   ['Check'       , 'Check'         , 'Check'      , 'Check'    , 'Check'      , 'Check'   , 'Fold'      , 'Fold'        , 'Fold'     , 'Fold'      , 'Fold' 		, 'Fold'    ]], #Conservative

#			  Bet216										     Diamonds , Clubs   , Hearts  , Spades
			  'decision_before_turn_highest_bet_royal_flush' : [['Raise'  , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  													['Raise'  , 'Raise' , 'Raise' , 'Raise'],  #Normal
			  												 	['Call'   , 'Call'  , 'Call'  , 'Call' ]], #Conservative

#			  Bet217												Diamonds High , Diamonds Medium , Diamonds Low , Clubs High , Clubs Medium , Clubs Low , Hearts High , Hearts Medium , Hearts Low , Spades High , Spades Medium , Spades Low
			  'decision_before_turn_highest_bet_straight_flush' : [['Raise'       , 'Raise'         , 'Raise'      , 'Raise' 	, 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 		, 'Raise'	],  #Aggressive
			  										   			   ['Call'        , 'Call'          , 'Call'       , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 		, 'Raise'   ],  #Normal
			  										   			   ['Call'        , 'Call'          , 'Call' 	   , 'Call'     , 'Call'       , 'Call'    , 'Call'      , 'Call'        , 'Call'     , 'Call'      , 'Call' 		, 'Call'	]], #Conservative

#			  Bet218												High    , Medium  , Low
			  'decision_before_turn_highest_bet_four_of_a_kind' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  										   			   ['Raise' , 'Raise' , 'Raise'],  #Normal
			  										   			   ['Call'  , 'Call'  , 'Call' ]], #Conservative

#			  Bet219 - Three of a Kind is:                   	High    , Medium  , Low
			  'decision_before_turn_highest_bet_full_house' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  									   			   ['Raise' , 'Raise' , 'Raise'],  #Normal
			  									   			   ['Call'  , 'Call'  , 'Call' ]], #Conservative

#			  Bet220 - High Card is:					   Diamonds High , Diamonds Medium , Diamonds Low , Clubs High , Clubs Medium , Clubs Low , Hearts High , Hearts Medium , Hearts Low , Spades High , Spades Medium , Spades Low
			  'decision_before_turn_highest_bet_flush' : [['Raise'       , 'Raise'         , 'Raise'      , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	   , 'Raise'   ],  #Aggressive
			  										   	  ['Call'        , 'Call'          , 'Call'       , 'Call'     , 'Call' 	  , 'Call'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'   ],  #Normal
			  										   	  ['Call'        , 'Call'          , 'Call' 	  , 'Call'     , 'Call'       , 'Call'    , 'Call'      , 'Call'        , 'Call'     , 'Call'      , 'Call' 	   , 'Call'	   ]], #Conservative

#			  Bet221										  Diamonds High , Diamonds Medium , Diamonds Low , Clubs High , Clubs Medium , Clubs Low , Hearts High , Hearts Medium , Hearts Low , Spades High , Spades Medium , Spades Low
			  'decision_before_turn_highest_bet_straight' : [['Raise'       , 'Raise'         , 'Raise'      , 'Raise' 	  , 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	  , 'Raise'	  ],  #Aggressive
			  										   	  	 ['Call'        , 'Call'          , 'Call'       , 'Call'     , 'Call'       , 'Call'    , 'Raise'     , 'Raise'       , 'Raise'    ,  'Raise'    , 'Raise' 	  , 'Raise'	  ],  #Normal
			  										   	  	 ['Call'        , 'Call'          , 'Call' 	     , 'Call'     , 'Call'       , 'Call'    , 'Call'      , 'Call'        , 'Call'     , 'Call'      , 'Call' 		  , 'Call'	  ]], #Conservative

#			  Bet222												 High    , Medium  , Low
			  'decision_before_turn_highest_bet_three_of_a_kind' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  													 	['Raise' , 'Raise' , 'Call' ],  #Normal
			  														['Call'  , 'Fold'  , 'Fold' ]], #Conservative

#			  Bet223										  High High , High Medium , High Low , Medium Medium , Medium Low , Low Low
			  'decision_before_turn_highest_bet_two_pair' : [['Raise'   , 'Raise'     , 'Raise'  , 'Raise'       , 'Raise'    , 'Raise' ],  #Aggressive
			  											  	 ['Raise'   , 'Raise'     , 'Raise'  , 'Call'        , 'Call'     , 'Call' ],  #Normal
			  											  	 ['Call'    , 'Call'      , 'Call'   , 'Fold'        , 'Fold'     , 'Fold'  ]], #Conservative

#			  Bet224										  High    , Medium  , Low
			  'decision_before_turn_highest_bet_one_pair' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  											  	 ['Raise' , 'Call'  , 'Call' ],  #Normal
			  												 ['Call'  , 'Fold'  , 'Fold' ]], #Conservative

#			  Bet225 - Number of in range cards:							 3       , 4
			  'decision_before_turn_highest_bet_in_range_of_royal_flush' : [['Raise' , 'Raise'],  #Aggressive
			  															 	['Call'  , 'Raise'],  #Normal
			  															 	['Fold'  , 'Call' ]], #Conservative

#			  Bet226															Diamonds , Clubs   , Hearts  , Spades
			  'decision_before_turn_highest_bet_in_range_of_straight_flush' : [['Raise'  , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  													   			   ['Call'   , 'Call'  , 'Raise' , 'Raise'],  #Normal
			  													   			   ['Call'   , 'Call'  , 'Call'  , 'Call' ]], #Conservative

#			  Bet227 - Number of in range cards:												3       , 4
			  'decision_before_turn_highest_bet_in_range_of_royal_flush_and_straight_flush' : [['Raise' , 'Raise'],  #Aggressive
			  																	   			   ['Raise' , 'Raise'],  #Normal
			  																	   			   ['Call'  , 'Call' ]], #Conservative

#			  Bet228												   Diamonds , Clubs   , Hearts  , Spades
			  'decision_before_turn_highest_bet_in_range_of_flush' : [['Raise'  , 'Raise' , 'Raise' , 'Raise'],  #Aggressive
			  													   	  ['Call'   , 'Call'  , 'Raise' , 'Raise'],  #Normal
			  													   	  ['Call'   , 'Call'  , 'Call'  , 'Call' ]], #Conservative   
												  
#			  Bet229										  			  3        , 4 
			  'decision_before_turn_highest_bet_in_range_of_straight' : [['Raise' , 'Raise'],  #Aggressive
			  												 			 ['Call'  , 'Raise'],  #Normal
			  												 			 ['Fold'  , 'Call' ]], #Conservative

#			  Bet230 - Highest Card is:								   Diamonds High , Diamonds Medium , Diamonds Low , Clubs High , Clubs Medium , Clubs Low , Hearts High , Hearts Medium , Hearts Low , Spades High , Spades Medium , Spades Low
			  'decision_before_turn_highest_bet_all_distinct_cards' : [['Raise'       , 'Raise'         , 'Raise'      , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise' 	   , 'Raise'   ],  #Aggressive
			  										   				  ['Call'        , 'Call'          , 'Call'       , 'Call'     , 'Call'       , 'Call'    , 'Call'      , 'Call'        , 'Call'     , 'Call'      , 'Call' 	   , 'Call'	   ],  #Normal
			  										   				  ['Fold'        , 'Fold'          , 'Fold'       , 'Fold'     , 'Fold'       , 'Fold'    , 'Fold'      , 'Fold' 		, 'Fold'     ,'Call'       , 'Call'        , 'Call'    ]], #Conservative

#														 Spades  , Hearts  , Clubs   , Diamonds
			  'decision_before_showdown_royal_flush' : [['Raise' , 'Raise' , 'Raise' , 'Raise' ],  #Aggressive
			  											['Raise' , 'Raise' , 'Raise' , 'Raise' ],  #Normal
			  											['Check' , 'Check' , 'Check' , 'Check' ]], #Conservative

#														    Spades High , Spades Medium , Spades Low , Hearts High , Hearts Medium , Hearts Low , Clubs High , Clubs Medium , Clubs Low , Diamonds High , Diamonds Medium , Diamonds Low
			  'decision_before_showdown_straight_flush' : [['Raise'     , 'Raise'       , 'Raise'    , 'Raise' 	   , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise' 		  , 'Raise'		],  #Aggressive
			  										   	   ['Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise' 		  , 'Raise'		],  #Normal
			  										   	   ['Check'     , 'Check'       , 'Check' 	 , 'Check'     , 'Check'       , 'Check'    , 'Check'    , 'Check'      , 'Check'   , 'Check'       , 'Check' 		  , 'Check'		]], #Conservative

#															High    , Medium  , Low
			  'decision_before_showdown_four_of_a_kind' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  											   ['Raise' , 'Raise' , 'Raise'],  #Normal
			  											   ['Check' , 'Check' , 'Check']], #Conservative

#			  Three of a Kind is:						High    , Medium  , Low
			  'decision_before_showdown_full_house' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  									   	   ['Raise' , 'Raise' , 'Raise'],  #Normal
			  									   	   ['Check' , 'Check' , 'Check']], #Conservative

#												   Spades High , Spades Medium , Spades Low , Hearts High , Hearts Medium , Hearts Low , Clubs High , Clubs Medium , Clubs Low , Diamonds High , Diamonds Medium , Diamonds Low
			  'decision_before_showdown_flush' : [['Raise'     , 'Raise'       , 'Raise'    , 'Raise' 	  , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise' 		 , 'Raise'		],  #Aggressive
			  									  ['Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Check'    , 'Check'      , 'Check'   , 'Check'       , 'Check' 		 , 'Check'		],  #Normal
			  									  ['Check'     , 'Check'       , 'Check' 	, 'Check'     , 'Check'       , 'Check'    , 'Check'    , 'Check'      , 'Check'   , 'Check'       , 'Check' 		 , 'Check'		]], #Conservative

#													  Spades High , Spades Medium , Spades Low , Hearts High , Hearts Medium , Hearts Low , Clubs High , Clubs Medium , Clubs Low , Diamonds High , Diamonds Medium , Diamonds Low
			  'decision_before_showdown_straight' : [['Raise'     , 'Raise'       , 'Raise'    , 'Raise' 	 , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise' 		, 'Raise'	   ],  #Aggressive
			  										 ['Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Check'    , 'Check'      , 'Check'   , 'Check'       , 'Check' 		, 'Check'	   ],  #Normal
			  										 ['Check'     , 'Check'       , 'Check'    , 'Check'     , 'Check'       , 'Check'    , 'Check'    , 'Check'      , 'Check'   , 'Check'       , 'Check' 		, 'Check'	   ]], #Conservative

#															 High    , Medium  , Low
			  'decision_before_showdown_three_of_a_kind' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  												['Raise' , 'Raise' , 'Check'],  #Normal
			  												['Check' , 'Check' , 'Check']], #Conservative

#													  High High , High Medium , High Low , Medium Medium , Medium Low , Low Low
			  'decision_before_showdown_two_pair' : [['Raise'   , 'Raise'     , 'Raise'  , 'Raise'       , 'Raise'    , 'Raise'],  #Aggressive
			  										 ['Raise'   , 'Raise'     , 'Raise'  , 'Check'       , 'Check'    , 'Check'],  #Normal
			  										 ['Check'   , 'Check'     , 'Check'  , 'Fold'        , 'Fold'     , 'Fold' ]], #Conservative

#													  High    , Medium  , Low
			  'decision_before_showdown_one_pair' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  										 ['Raise' , 'Check' , 'Check'],  #Normal
			  										 ['Check' , 'Fold'  , 'Fold' ]], #Conservative

#													   Spades High , Spades Medium , Spades Low , Hearts High , Hearts Medium , Hearts Low , Clubs High , Clubs Medium , Clubs Low , Diamonds High , Diamonds Medium , Diamonds Low
			  'decision_before_showdown_high_card' : [['Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise'         , 'Raise'     ],  #Aggressive
			  										  ['Check'     , 'Check'       , 'Check'    , 'Check'     , 'Check'       , 'Check'    , 'Check'    , 'Check'      , 'Check'   , 'Check'       , 'Check'         , 'Check'     ],  #Normal
			  										  ['Fold'      , 'Fold'        , 'Fold'     , 'Fold'      , 'Fold'        , 'Fold'     , 'Fold'     , 'Fold'       , 'Fold'    , 'Fold'        , 'Fold'          , 'Fold'      ]], #Conservative

#														 			 Spades  , Hearts  , Clubs   , Diamonds
			  'decision_before_showdown_highest_bet_royal_flush' : [['Raise' , 'Raise' , 'Raise' , 'Raise' ],  #Aggressive
			  														['Raise' , 'Raise' , 'Raise' , 'Raise' ],  #Normal
			  														['Call'  , 'Call'  , 'Call'  , 'Call'  ]], #Conservative

#														    			Spades High , Spades Medium , Spades Low , Hearts High , Hearts Medium , Hearts Low , Clubs High , Clubs Medium , Clubs Low , Diamonds High , Diamonds Medium , Diamonds Low
			  'decision_before_showdown_highest_bet_straight_flush' : [['Raise'     , 'Raise'       , 'Raise'    , 'Raise' 	   , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise' 		  , 'Raise'		],  #Aggressive
			  										   	   			   ['Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise' 		  , 'Raise'		],  #Normal
			  										   	  			   ['Call'      , 'Call'        , 'Call' 	 , 'Call'      , 'Call'        , 'Call'     , 'Call'     , 'Call'       , 'Call'    , 'Call'        , 'Call' 		  , 'Call'		]], #Conservative

#																		High    , Medium  , Low
			  'decision_before_showdown_highest_bet_four_of_a_kind' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  											   			   ['Raise' , 'Raise' , 'Raise'],  #Normal
			  											   			   ['Call'  , 'Call'  , 'Call' ]], #Conservative

#			  Three of a Kind is:									High    , Medium  , Low
			  'decision_before_showdown_highest_bet_full_house' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  									   	   			   ['Raise' , 'Raise' , 'Raise'],  #Normal
			  									   	   			   ['Call'  , 'Call'  , 'Call' ]], #Conservative

#												  			   Spades High , Spades Medium , Spades Low , Hearts High , Hearts Medium , Hearts Low , Clubs High , Clubs Medium , Clubs Low , Diamonds High , Diamonds Medium , Diamonds Low
			  'decision_before_showdown_highest_bet_flush' : [['Raise'     , 'Raise'       , 'Raise'    , 'Raise' 	  , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise' 		 , 'Raise'		],  #Aggressive
			  									  			  ['Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Call'     , 'Call'       , 'Call'    , 'Call'        , 'Call' 		 , 'Call'		],  #Normal
			  									  			  ['Call'      , 'Call'        , 'Call' 	, 'Call'      , 'Call'        , 'Call'     , 'Call'     , 'Call'       , 'Call'    , 'Call'        , 'Call' 		 , 'Call'		]], #Conservative

#													 			  Spades High , Spades Medium , Spades Low , Hearts High , Hearts Medium , Hearts Low , Clubs High , Clubs Medium , Clubs Low , Diamonds High , Diamonds Medium , Diamonds Low
			  'decision_before_showdown_highest_bet_straight' : [['Raise'     , 'Raise'       , 'Raise'    , 'Raise' 	 , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise' 		, 'Raise'	   ],  #Aggressive
			  										 			 ['Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Call'     , 'Call'       , 'Call'    , 'Call'        , 'Call' 		    , 'Call'	   ],  #Normal
			  										 			 ['Call'      , 'Call'        , 'Call'     , 'Call'      , 'Call'        , 'Call'     , 'Call'     , 'Call'       , 'Call'    , 'Call'        , 'Call' 		    , 'Call'	   ]], #Conservative

#																		 High    , Medium  , Low
			  'decision_before_showdown_highest_bet_three_of_a_kind' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  															['Raise' , 'Raise' , 'Call' ],  #Normal
			  															['Call'  , 'Call'  , 'Fold' ]], #Conservative

#													  			  High High , High Medium , High Low , Medium Medium , Medium Low , Low Low
			  'decision_before_showdown_highest_bet_two_pair' : [['Raise'   , 'Raise'     , 'Raise'  , 'Raise'       , 'Raise'    , 'Raise'],  #Aggressive
			  										 			 ['Raise'   , 'Raise'     , 'Raise'  , 'Call'        , 'Call'     , 'Call' ],  #Normal
			  										 			 ['Call'    , 'Call'      , 'Call'   , 'Fold'        , 'Fold'     , 'Fold' ]], #Conservative

#													  			  High    , Medium  , Low
			  'decision_before_showdown_highest_bet_one_pair' : [['Raise' , 'Raise' , 'Raise'],  #Aggressive
			  										 			 ['Raise' , 'Call'  , 'Call' ],  #Normal
			  										 			 ['Call'  , 'Fold'  , 'Fold' ]], #Conservative

#													   			   Spades High , Spades Medium , Spades Low , Hearts High , Hearts Medium , Hearts Low , Clubs High , Clubs Medium , Clubs Low , Diamonds High , Diamonds Medium , Diamonds Low
			  'decision_before_showdown_highest_bet_high_card' : [['Raise'     , 'Raise'       , 'Raise'    , 'Raise'     , 'Raise'       , 'Raise'    , 'Raise'    , 'Raise'      , 'Raise'   , 'Raise'       , 'Raise'         , 'Raise'     ],  #Aggressive
			  										  			  ['Call'      , 'Call'        , 'Call'     , 'Call'      , 'Call'        , 'Call'     , 'Call'     , 'Call'       , 'Call'    , 'Call'        , 'Call'          , 'Call'      ],  #Normal
			  										  			  ['Fold'      , 'Fold'        , 'Fold'     , 'Fold'      , 'Fold'        , 'Fold'     , 'Fold'     , 'Fold'       , 'Fold'    , 'Fold'        , 'Fold'          , 'Fold'      ]], #Conservative
												  } 

#create the appropriate dictionaries for a game of 9 players
def define_players():
	global l_players
	l_players.append({'Order' : 0, 'Name' : 'Alice', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
													'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0,
													'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	l_players.append({'Order' : 1, 'Name' : 'Bob', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
									  			   'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0, 
									  			   'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	l_players.append({'Order' : 2, 'Name' : 'Charlie', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
										 			   'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0,
										  			   'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	l_players.append({'Order' : 3, 'Name' : 'David', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
													 'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0,
													 'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	l_players.append({'Order' : 4, 'Name' : 'Eli', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
													 'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0,
													 'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	l_players.append({'Order' : 5, 'Name' : 'Frank', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
													 'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0,
													 'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	l_players.append({'Order' : 6, 'Name' : 'Grace', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
													 'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0,
													 'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	l_players.append({'Order' : 7, 'Name' : 'Harry', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
													 'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0,
													 'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	l_players.append({'Order' : 8, 'Name' : 'Ivan', 'Card1_Number' : 0, 'Card1_Value' : '*', 'Card1_Suite' : '*', 'Card1_Weight' : 0,
													 'Card2_Number' : 0, 'Card2_Value' : '*', 'Card2_Suite' : '*', 'Card2_Weight' : 0,
													 'Money' : player_buyin_amount, 'Player_Type' : 'Normal'})
	
#get player names and which are human if any
def get_player_names():
	global l_players
	global human_players
	more_players = 1
	current_player_name = ''
	player_list = []
	for num in range(0,len(l_players)):
		l_players[num]['Name'] = input('Enter Player ' + str(num + 1) + ' Name: ')
		player_list.append(l_players[num]['Name'].upper())

	print()
	print('Enter the names of players that are human.')
	print('Press enter after each name.')
	print('If there are no more human players, just enter 0.')
	#setting human player type
	while (more_players != 0):	
		print()
		current_player_name = input('Enter player name here: ')
		if current_player_name != '0':
			while (current_player_name.upper() not in player_list) or (current_player_name in human_players):
				if current_player_name == '0':
					more_players = 0
					break
				if current_player_name.upper() not in player_list:
					print()
					print('There is no player by that name in this game.')
					print("Please enter a valid player's name.")
					current_player_name = input('Enter player name here: ')
				elif current_player_name in human_players:
					print()
					print('That player has already been converted to a human player.')
					print("Please enter a different player's name.")
					current_player_name = input('Enter player name here: ')
			for player in l_players:
				if player['Name'].upper() == current_player_name.upper():
					player['Player_Type'] = 'Human'
					human_players.append(current_player_name)
					print()
					print(player['Name'] + ' is now stored as a human player.')
			if len(human_players) == len(player_list):
				break
		else:
			more_players = 0

	print()
	if len(human_players) == 0:
		print('There are no human players in this game.')
	elif len(human_players) == 1:
		print('The human player in this game is ' + human_players[0] + '.')
	elif len(human_players) == len(player_list):
		print('All the players in this game are human players.')
	else:
		print('The human players in this game are ', end = "")
		for element in human_players:
			if human_players.index(element) == len(human_players) - 1:
				print('and ' + element + '.')
			else:
				print(element + ', ', end = "")
	print('Press enter to begin the game.')
	input()
	
#randomly assign player types to non-human players
def randomly_assign_player_types():
	global l_players
	for num in range(0,len(l_players)):
		if l_players[num]['Player_Type'] != 'Human':
			l_players[num]['Player_Type'] = random.choice(player_type_list)

#create the deck with all 52 cards
def make_deck():
	global l_deck
	l_deck.append({'Number': 1, 'Value': 'A', 'Suite': 'S', 'Weight': 2653})
	l_deck.append({'Number': 2, 'Value': '2', 'Suite': 'S', 'Weight': 157})
	l_deck.append({'Number': 3, 'Value': '3', 'Suite': 'S', 'Weight': 365})
	l_deck.append({'Number': 4, 'Value': '4', 'Suite': 'S', 'Weight': 573})
	l_deck.append({'Number': 5, 'Value': '5', 'Suite': 'S', 'Weight': 781})
	l_deck.append({'Number': 6, 'Value': '6', 'Suite': 'S', 'Weight': 989})
	l_deck.append({'Number': 7, 'Value': '7', 'Suite': 'S', 'Weight': 1197})
	l_deck.append({'Number': 8, 'Value': '8', 'Suite': 'S', 'Weight': 1405})
	l_deck.append({'Number': 9, 'Value': '9', 'Suite': 'S', 'Weight': 1613})
	l_deck.append({'Number': 10, 'Value': '10', 'Suite': 'S', 'Weight': 1821})
	l_deck.append({'Number': 11, 'Value': 'J', 'Suite': 'S', 'Weight': 2029})
	l_deck.append({'Number': 12, 'Value': 'Q', 'Suite': 'S', 'Weight': 2237})
	l_deck.append({'Number': 13, 'Value': 'K', 'Suite': 'S', 'Weight': 2445})
	l_deck.append({'Number': 14, 'Value': 'A', 'Suite': 'H', 'Weight': 2601})
	l_deck.append({'Number': 15, 'Value': '2', 'Suite': 'H', 'Weight': 105})
	l_deck.append({'Number': 16, 'Value': '3', 'Suite': 'H', 'Weight': 313})
	l_deck.append({'Number': 17, 'Value': '4', 'Suite': 'H', 'Weight': 521})
	l_deck.append({'Number': 18, 'Value': '5', 'Suite': 'H', 'Weight': 729})
	l_deck.append({'Number': 19, 'Value': '6', 'Suite': 'H', 'Weight': 937})
	l_deck.append({'Number': 20, 'Value': '7', 'Suite': 'H', 'Weight': 1145})
	l_deck.append({'Number': 21, 'Value': '8', 'Suite': 'H', 'Weight': 1353})
	l_deck.append({'Number': 22, 'Value': '9', 'Suite': 'H', 'Weight': 1561})
	l_deck.append({'Number': 23, 'Value': '10', 'Suite': 'H', 'Weight': 1769})
	l_deck.append({'Number': 24, 'Value': 'J', 'Suite': 'H', 'Weight': 1977})
	l_deck.append({'Number': 25, 'Value': 'Q', 'Suite': 'H', 'Weight': 2185})
	l_deck.append({'Number': 26, 'Value': 'K', 'Suite': 'H', 'Weight': 2393})
	l_deck.append({'Number': 27, 'Value': 'A', 'Suite': 'C', 'Weight': 2549})
	l_deck.append({'Number': 28, 'Value': '2', 'Suite': 'C', 'Weight': 53})
	l_deck.append({'Number': 29, 'Value': '3', 'Suite': 'C', 'Weight': 261})
	l_deck.append({'Number': 30, 'Value': '4', 'Suite': 'C', 'Weight': 469})
	l_deck.append({'Number': 31, 'Value': '5', 'Suite': 'C', 'Weight': 677})
	l_deck.append({'Number': 32, 'Value': '6', 'Suite': 'C', 'Weight': 885})
	l_deck.append({'Number': 33, 'Value': '7', 'Suite': 'C', 'Weight': 1093})
	l_deck.append({'Number': 34, 'Value': '8', 'Suite': 'C', 'Weight': 1301})
	l_deck.append({'Number': 35, 'Value': '9', 'Suite': 'C', 'Weight': 1509})
	l_deck.append({'Number': 36, 'Value': '10', 'Suite': 'C', 'Weight': 1717})
	l_deck.append({'Number': 37, 'Value': 'J', 'Suite': 'C', 'Weight': 1925})
	l_deck.append({'Number': 38, 'Value': 'Q', 'Suite': 'C', 'Weight': 2133})
	l_deck.append({'Number': 39, 'Value': 'K', 'Suite': 'C', 'Weight': 2341})
	l_deck.append({'Number': 40, 'Value': 'A', 'Suite': 'D', 'Weight': 2497})
	l_deck.append({'Number': 41, 'Value': '2', 'Suite': 'D', 'Weight': 1})
	l_deck.append({'Number': 42, 'Value': '3', 'Suite': 'D', 'Weight': 209})
	l_deck.append({'Number': 43, 'Value': '4', 'Suite': 'D', 'Weight': 417})
	l_deck.append({'Number': 44, 'Value': '5', 'Suite': 'D', 'Weight': 625})
	l_deck.append({'Number': 45, 'Value': '6', 'Suite': 'D', 'Weight': 833})
	l_deck.append({'Number': 46, 'Value': '7', 'Suite': 'D', 'Weight': 1041})
	l_deck.append({'Number': 47, 'Value': '8', 'Suite': 'D', 'Weight': 1249})
	l_deck.append({'Number': 48, 'Value': '9', 'Suite': 'D', 'Weight': 1457})
	l_deck.append({'Number': 49, 'Value': '10', 'Suite': 'D', 'Weight': 1665})
	l_deck.append({'Number': 50, 'Value': 'J', 'Suite': 'D', 'Weight': 1873})
	l_deck.append({'Number': 51, 'Value': 'Q', 'Suite': 'D', 'Weight': 2081})
	l_deck.append({'Number': 52, 'Value': 'K', 'Suite': 'D', 'Weight': 2289})
	
#determine which players put the big blind and small blind
def determine_blinds():
	global dealer_order
	global big_blind
	global small_blind
	global player_count
	if dealer_order >= len(l_players) - 1:
		dealer_order = 0
	small_blind = 0 if dealer_order + 1 > len(l_players) - 1 else dealer_order + 1
	big_blind = 0 if small_blind + 1 > len(l_players) - 1 else small_blind + 1

#get the value of the current pot
def get_current_pot():	
	global betting_temp_player_list
	global l_players
	current_pot = 0
	for player in betting_temp_player_list:
		current_pot += player['Money']
		#for player1 in l_players:
		#	if player['Name'] == player1['Name']:
		#		player1['Money'] -= player['Money']
		#		break
	return current_pot

#redistributing money to people
def redistribute_money(extra_money,skip_betting,last_player_to_raise):
	global betting_temp_player_list

	extra_money_value = 0
	player_who_put_all_in = ''
	count = 0
	redistributed_players = []

	for num in extra_money:
		if num > extra_money_value:
			extra_money_value = num

	for num in extra_money:
		if num == extra_money_value:
			player_who_put_all_in = betting_temp_player_list[count]['Name']
		count += 1

	player_found = False
	broke_out = False
	if extra_money_value != 0:
		skip_betting = True
		for player in betting_temp_player_list:
			if player_found == True:
				if player['Name'] == player_who_put_all_in:
					player['Money'] -= extra_money_value
					broke_out = True
					redistributed_players.append(player['Name'])
					break
				else:
					if player['Folded?'] != True:
						player['Money'] -= extra_money_value
			else:
				if player['Name'] == last_player_to_raise:
					player_found = True
					redistributed_players.append(player['Name'])
					player['Money'] -= extra_money_value

		if broke_out != True:
			for player in betting_temp_player_list:
				if player['Name'] == player_who_put_all_in:
					player['Money'] -= extra_money_value
					redistributed_players.append(player['Name'])
					break
				else:
					if player['Folded?'] != True:
						player['Money'] -= extra_money_value
						redistributed_players.append(player['Name'])

	count = 0
	for player in betting_temp_player_list:
		if (player['Name'] not in redistributed_players) and (extra_money[count] > 0):
			player['Money'] -= extra_money_value
		count += 1

	return skip_betting
	
#deal one card
def deal_card():
	global l_deck
	global l_dealt_cards
	global value
	value = random.randint(1,52)
	while (l_deck[value - 1]) in l_dealt_cards:
		value = random.randint(1,52)
	l_dealt_cards.append(l_deck[value - 1])
	return l_deck[value - 1]
	
#deal 2 cards to each player in the game
def deal_cards_to_players():
	global player_count
	global l_players
	deal_card() #first folded card before dealing
	for player in l_players:
		card = deal_card()
		player['Card1_Number'] = card['Number']
		player['Card1_Value'] = card['Value']
		player['Card1_Suite'] = card['Suite']
	for player in l_players:
		card = deal_card()
		player['Card2_Number'] = card['Number']
		player['Card2_Value'] = card['Value']
		player['Card2_Suite'] = card['Suite']

#deal the three cards of the flop
def deal_flop():
	global community_cards
	for num in range(1,4):
		deal_card()
	for num in range(1,4):
		community_cards.append(deal_card())

#deal the card of the turn/river
def deal_turn_or_river():
	global community_cards
	deal_card()
	community_cards.append(deal_card())

#show a single card
def print_card(card):
	card = card['Value'] + '-' + card['Suite'] if card['Value'] == '10' else ' ' + card['Value'] + '-' + card['Suite']
	return card

#show a player with their corresponding cards
def print_player(player):
	print(player['Name'] + ': ' + (' ' * (7 - len(player['Name']))), end = " ")
	if player['Card1_Value'] != '10':
		print('', end = " ")
	print(player['Card1_Value'] + '-' + player['Card1_Suite'] + ' ', end = " ")
	if player['Card2_Value'] != '10':
		print('', end = " ")
	print(player['Card2_Value'] + '-' + player['Card2_Suite'] + ' ')

#show the community cards
def print_community_cards():
	global community_cards
	print('Community cards:')
	print()
	if len(community_cards) == 0:
		return
	elif len(community_cards) >= 3:
		print('The flop', end = "   ")
		for num in range(1,4):
			if num == 3:
				print(print_card(community_cards[num - 1]))
			else:
				print(print_card(community_cards[num - 1]), end = "  ")
		if len(community_cards) == 4:
			print('The turn', end = "   ")
			print(print_card(community_cards[3]))
		elif len(community_cards) == 5:
			print('The turn', end = "   ")
			print(print_card(community_cards[3]))
			print('The river', end = "  ")
			print(print_card(community_cards[4]))

#show human player their cards
def print_player_cards(player):
	print('Your cards: ' + player['Card1_Value'] + '-' + player['Card1_Suite'] + ' ' + player['Card2_Value'] + '-' + player['Card2_Suite'])

#show flop cards
def print_flop():
	global community_cards
	print('The flop:  ' + print_card(community_cards[0]) + ' ' + print_card(community_cards[1]) + ' ' + print_card(community_cards[2]))

#show turn card
def print_turn():
	global community_cards
	print('The turn:  ' + print_card(community_cards[3]))

#show river card
def print_river():
	global community_cards
	print('The river: ' + print_card(community_cards[4]))
		
#make a list of the players playing in this hand (pre-flop)
def make_temp_player_list():
	global betting_temp_player_list
	global dealer_order
	global l_players
	global big_blind
	global small_blind
	global big_blind_amount
	global small_blind_amount

	starting_appended = False
	betting_temp_player_list = []
	for player in l_players:
		if starting_appended == False:
			if player['Order'] == big_blind + 1:
				starting_appended = True
				betting_temp_player_list.append({'Order' : player['Order'], 'Name' : player['Name'], 'Card1_Value' : player['Card1_Value'], 'Card1_Suite' : player['Card1_Suite'], 'Card1_Number' : player['Card1_Number'], 'Card1_Weight' : player['Card1_Weight'],
																										'Card2_Value' : player['Card2_Value'], 'Card2_Suite' : player['Card2_Suite'], 'Card2_Number' : player['Card2_Number'], 'Card2_Weight' : player['Card2_Weight'],
																										'Money' : 0, 'Raised?' : False, 'Folded?' : False, 'Called?' : False, 'Player_Type' : player['Player_Type'], 'Decision' : '', 'Function' : '', 'Balance' : player['Money']})
		elif starting_appended == True:
			betting_temp_player_list.append({'Order' : player['Order'], 'Name' : player['Name'], 'Card1_Value' : player['Card1_Value'], 'Card1_Suite' : player['Card1_Suite'], 'Card1_Number' : player['Card1_Number'], 'Card1_Weight' : player['Card1_Weight'],
																	  							 'Card2_Value' : player['Card2_Value'], 'Card2_Suite' : player['Card2_Suite'], 'Card2_Number' : player['Card2_Number'], 'Card2_Weight' : player['Card2_Weight'],
																  	 							 'Money' : 0, 'Raised?' : False, 'Folded?' : False, 'Called?' : False, 'Player_Type' : player['Player_Type'], 'Decision' : '', 'Function' : '', 'Balance' : player['Money']})
	
	for player in l_players:
		if player['Order'] != big_blind + 1:
			betting_temp_player_list.append({'Order' : player['Order'], 'Name' : player['Name'], 'Card1_Value' : player['Card1_Value'], 'Card1_Suite' : player['Card1_Suite'], 'Card1_Number' : player['Card1_Number'], 'Card1_Weight' : player['Card1_Weight'],
																	  							 'Card2_Value' : player['Card2_Value'], 'Card2_Suite' : player['Card2_Suite'], 'Card2_Number' : player['Card2_Number'], 'Card2_Weight' : player['Card2_Weight'],
																  	 							 'Money' : 0, 'Raised?' : False, 'Folded?' : False, 'Called?' : False, 'Player_Type' : player['Player_Type'], 'Decision' : '', 'Function' : '', 'Balance' : player['Money']})
		elif player['Order'] == big_blind + 1:
			break

	for player in betting_temp_player_list:
		if player['Order'] == big_blind:
			if player['Balance'] < big_blind_amount:
				big_blind_amount = player['Balance']
				small_blind_amount = int(big_blind_amount / 2)
			player['Money'] = big_blind_amount
			break

		if player['Order'] == small_blind:
			if player['Balance'] < small_blind_amount:
				small_blind_amount = player['Balance']
				big_blind_amount = int(small_blind_amount * 2)
			player['Money'] = small_blind_amount
			break

#make a list of the players playing in this hand (flop and beyond)
def make_temp_player_list2():
	global betting_temp_player_list
	global dealer_order
	global l_players
	global big_blind
	global small_blind
	global big_blind_amount
	global small_blind_amount

	starting_appended = False
	new_betting_temp_player_list = []
	for player in betting_temp_player_list:
		if starting_appended == False:
			if player['Order'] == small_blind:
				starting_appended = True
				new_betting_temp_player_list.append(player)
		elif starting_appended == True:
			new_betting_temp_player_list.append(player)
	
	for player in betting_temp_player_list:
		if player['Order'] != small_blind:
			new_betting_temp_player_list.append(player)
		elif player['Order'] == small_blind:
			break

	for player in new_betting_temp_player_list:
		if player['Order'] == big_blind:
			if player['Balance'] < big_blind_amount:
				big_blind_amount = player['Balance']
				small_blind_amount = int(big_blind_amount / 2)
			player['Money'] = big_blind_amount
			break

		if player['Order'] == small_blind:
			if player['Balance'] < small_blind_amount:
				small_blind_amount = player['Balance']
				big_blind_amount = int(small_blind_amount * 2)
			player['Money'] = small_blind_amount
			break

	betting_temp_player_list = new_betting_temp_player_list

#determine index corresponding to player type
def determine_player_type_indexes(player):
	if player['Player_Type'] == 'Aggressive':
		player_type_index = 0
	elif player['Player_Type'] == 'Normal':
		player_type_index = 1
	elif player['Player_Type'] == 'Conservative':
		player_type_index = 2
	elif player['Player_Type'] == 'Human':
		player_type_index = 3
	return player_type_index

#human player decision
def human_player_decision_making(player,highest_bet,round_one_yes,last_player_to_raise,amount_to_match):
	global betting_temp_player_list
	global big_blind
	global small_blind
	global raise_amount
	possible_decisions = []
	decision = ''
	if highest_bet != True:
		possible_decisions.append('Raise')
	if (((round_one_yes == True) and (player['Order'] == big_blind)) and (last_player_to_raise == '')) or ((round_one_yes != True) and (last_player_to_raise == '')):
		possible_decisions.append('Check')
	if ((round_one_yes == True) and (player['Order'] != big_blind)) or (last_player_to_raise != ''):
		possible_decisions.append('Call')
	possible_decisions.append('Fold')

	#make the decision
	print()
	print('Enter the corresponding number of your decision: ')
	for num in range(0,len(possible_decisions)):
		if possible_decisions[num] == 'Raise':
			print(str(num + 1) + '. ' + possible_decisions[num] + ' by ' + str(raise_amount))
		elif possible_decisions[num] == 'Call':
			print(str(num + 1) + '. ' + possible_decisions[num] + ' - put in ' + str(amount_to_match - player['Money']))
		else:
			print(str(num + 1) + '. ' + possible_decisions[num])
	print()
	decision = input()
	while (int(decision) not in range(1,len(possible_decisions) + 1)):
		print('That is not a valid response. Please enter a decision that is given as an option.')
		decision = input()
	player['Decision'] = possible_decisions[int(decision) - 1]

#clear ONLY decision, function, Raised?, and Called? between rounds of bettings in same hand
def clear_temp_list():
	global betting_temp_player_list
	for player in betting_temp_player_list:
		player['Decision'] = ''
		player['Function'] = ''
		#player['Money'] = 0
		player['Raised?'] = False
		#player['Folded?'] = False
		player['Called?'] = False

#actual decision making process (for every round of betting for every player)
def bet(player,amount_to_match,last_player_to_raise,highest_bet,round_one_yes,round_round_one_yes,first_hand_yes,round_number):
	global raise_amount
	global betting_temp_player_list
	global big_blind_amount
	global small_blind_amount
	global big_blind
	global small_blind
	global player_buyin_amount
	global folded_players
	global pot
	extra_money_value = 0
	if round_number == 2:
		print_flop()
	if round_number == 3:
		print_flop()
		print_turn()
	elif round_number == 4:
		print_flop()
		print_turn()
		print_river()
	if player['Player_Type'] == 'Human' and player['Folded?'] == False:
		print_player_cards(player)
		if player['Name'] not in folded_players:
			human_player_decision_making(player,highest_bet,round_one_yes,last_player_to_raise,amount_to_match)
	if player['Decision'] == 'Raise':
		if highest_bet == True:
			player['Decision'] = 'Call'
		else:
			if round_one_yes == True:
				if player['Money'] + amount_to_match + raise_amount <= player['Balance']:
					#print('VISHWA ' + str(player['Money']) + ', ' + str(amount_to_match) + ', ' + str(raise_amount) + ', ' + str(player['Balance']))
					amount_to_match += raise_amount
					player['Money'] += amount_to_match - player['Money']
					#if round_round_one_yes == True:
					#	if player['Order'] == small_blind:
					#		player['Money'] -= small_blind_amount
					#	elif player['Order'] == big_blind:
					#		player['Money'] -= big_blind_amount
					last_player_to_raise = player['Name']
				else:
					if last_player_to_raise == '':
						player['Decision'] = 'Check'
					else:
						player['Decision'] = 'Call'
			else:
				if amount_to_match + raise_amount <= player['Balance']:
					amount_to_match += raise_amount
					player['Money'] += amount_to_match - player['Money']
					if round_round_one_yes == True:
						if player['Order'] == small_blind:
							player['Money'] -= small_blind_amount
						elif player['Order'] == big_blind:
							player['Money'] -= big_blind_amount
					last_player_to_raise = player['Name']
				else:
					if last_player_to_raise == '':
						player['Decision'] = 'Check'
					else:
						player['Decision'] = 'Call'
	if player['Decision'] == 'Call':
		if amount_to_match <= player['Balance']:
			if round_round_one_yes == True:
				if last_player_to_raise == '' and player['Order'] == big_blind:
					player['Decision'] = 'Check'
				elif player['Order'] == big_blind:
					player['Money'] += amount_to_match - player['Money']
				elif player['Order'] == small_blind:
					player['Money'] += amount_to_match - player['Money']
				else:
					player['Money'] += amount_to_match - player['Money']
			else:
				if last_player_to_raise == '':
					player['Decision'] = 'Check'
				else:
					player['Money'] += amount_to_match - player['Money']
		extra_money_value += (player['Money'] + (amount_to_match - player['Money'])) - player['Balance']
		player['Money'] += amount_to_match - player['Money']
		if player['Money'] >= player['Balance']:
			skip_betting = True
	if player['Decision'] == 'Check':
		player['Money'] += 0
	if player['Decision'] == 'Fold':
		player['Folded?'] = True
	if (player['Decision'] == 'Fold') and (player['Name'] not in folded_players):
		print(player['Name'] + ' ' + player['Decision'] + 's.')
	elif player['Decision'] != 'Fold':
		print(player['Name'] + ' ' + player['Decision'] + 's.')
	if player['Decision'] == 'Raise':
		print('Amount to Match: ' + str(amount_to_match))
	if player['Decision'] == 'Fold':
		folded_players.append(player['Name'])
	else:
		print(player['Name'] + ' = $' + str(player['Money']) + ' till now.')
		pot = get_current_pot()
		print('Pot: ' + str(pot))
	print()
	time.sleep(0.5)
	return [amount_to_match,last_player_to_raise,extra_money_value]

### Q LEARNING IMPLEMENTATION ###
## START ##

	# SOME NOTES:

		# THE STATE - defined in terms of each player
		# Each player will have a designated spot in the q-table
		# Function to create q-table will be called at the beginning of every single round of betting

		# THE ACTION - determined at the beginning of each round of betting

		# THE REWARD - expressed as the sum of the following (objective standpoint):
		#   (pot value - player's amount put in) 
		#   - (combined weight of two cards)
		#   (2000 / (13 - value_index)) if the two pocket cards are same value else (1000 / (value_index difference))
		#   (100 if the two pocket cards are the same suite)
		#   - (100 * (index of hand ranking)) if bet4

class Q_Learning():
	def __init__(self, current_player, betting_round, is_round_one, last_player_to_raise, amount_to_match, player_order, all_in):
		global betting_temp_player_list
		global community_cards
		global dealer_order
		global big_blind
		global small_blind
		global pot
		global raise_amount
		global folded_players
		self.orig_betting_temp_player_list = copy.deepcopy(betting_temp_player_list)
		self.orig_current_player = copy.deepcopy(current_player)
		self.orig_betting_round = copy.deepcopy(betting_round)
		self.orig_is_round_one = copy.deepcopy(is_round_one)
		self.orig_last_player_to_raise = copy.deepcopy(last_player_to_raise)
		self.orig_amount_to_match = copy.deepcopy(amount_to_match)
		self.orig_player_order = copy.deepcopy(player_order)
		self.orig_pot = copy.deepcopy(pot)
		self.orig_folded_players = copy.deepcopy(folded_players)
		self.orig_all_in = copy.deepcopy(all_in)
		self.betting_temp_player_list = betting_temp_player_list
		self.community_cards = community_cards
		self.dealer_order = dealer_order
		self.big_blind = big_blind
		self.small_blind = small_blind
		self.pot = pot
		self.raise_amount = raise_amount
		self.betting_round = betting_round
		self.is_round_one = is_round_one
		self.current_player = current_player
		self.player_order = player_order
		self.last_player_to_raise = last_player_to_raise
		self.folded_players = folded_players
		for player in betting_temp_player_list:
			if player['Name'] == self.current_player:
				self.player_order = betting_temp_player_list.index(player)
		self.amount_to_match = amount_to_match
		self.all_in = all_in

	# reset the simulation back to how it was
	def reset(self):
		global betting_temp_player_list
		global community_cards
		global dealer_order
		global big_blind
		global small_blind
		global pot
		global raise_amount
		global folded_players
		self.temp_betting_temp_player_list = copy.deepcopy(self.orig_betting_temp_player_list)
		self.temp_current_player = copy.deepcopy(self.orig_current_player)
		self.temp_betting_round = copy.deepcopy(self.orig_betting_round)
		self.temp_is_round_one = copy.deepcopy(self.orig_is_round_one)
		self.temp_last_player_to_raise = copy.deepcopy(self.orig_last_player_to_raise)
		self.temp_amount_to_match = copy.deepcopy(self.orig_amount_to_match)
		self.temp_player_order = copy.deepcopy(self.orig_player_order)
		self.temp_pot = copy.deepcopy(self.orig_pot)
		self.temp_folded_players = copy.deepcopy(self.orig_folded_players)
		self.temp_all_in = copy.deepcopy(self.orig_all_in)
		
		self.betting_temp_player_list = self.orig_betting_temp_player_list
		self.community_cards = community_cards
		self.dealer_order = dealer_order
		self.big_blind = big_blind
		self.small_blind = small_blind
		self.pot = self.orig_pot
		self.raise_amount = raise_amount
		self.betting_round = self.orig_betting_round
		self.is_round_one = self.orig_is_round_one
		self.current_player = self.orig_current_player
		self.player_order = self.orig_player_order
		self.last_player_to_raise = self.orig_last_player_to_raise
		self.folded_players = self.orig_folded_players
		for player in betting_temp_player_list:
			if player['Name'] == self.current_player:
				self.player_order = betting_temp_player_list.index(player)
		self.amount_to_match = self.orig_amount_to_match
		self.all_in = self.orig_all_in

		self.orig_betting_temp_player_list = self.temp_betting_temp_player_list
		self.orig_betting_round = self.temp_betting_round
		self.orig_is_round_one = self.temp_is_round_one
		self.orig_current_player = self.temp_current_player
		self.orig_player_order = self.temp_player_order
		self.orig_last_player_to_raise = self.temp_last_player_to_raise
		self.orig_folded_players = self.temp_folded_players
		self.orig_amount_to_match = self.temp_amount_to_match
		self.orig_all_in = self.temp_all_in

	# getting the actions
	def getPossibleActions(self):
		possible_actions = []
		if (self.is_round_one) and (self.betting_temp_player_list[self.player_order]['Balance'] - self.betting_temp_player_list[self.player_order]['Money'] - (self.amount_to_match - self.betting_temp_player_list[self.player_order]['Money']) >= self.raise_amount):
			possible_actions.append('Raise')
		if ((self.is_round_one and self.player_order == self.big_blind) and self.last_player_to_raise == '') or (not(self.is_round_one) and self.last_player_to_raise == ''):
			possible_actions.append('Check')
		if (self.is_round_one and self.player_order != self.big_blind) or self.last_player_to_raise != '':
			possible_actions.append('Call')
		possible_actions.append('Fold')
		return possible_actions

	# determine what hand a player has and return an appropriate increment
	def evaluate_hand(self):
		if (is_royal_flush(self.betting_temp_player_list[self.player_order])):
			combo = 'Royal Flush'
		elif (is_straight_flush(self.betting_temp_player_list[self.player_order])):
			combo = 'Straight Flush'
		elif (is_four_of_a_kind(self.betting_temp_player_list[self.player_order])):
			combo = 'Four of a Kind'
		elif (is_full_house(self.betting_temp_player_list[self.player_order])):
			combo = 'Full House'
		elif (is_flush(self.betting_temp_player_list[self.player_order])):
			combo = 'Flush'
		elif (is_straight(self.betting_temp_player_list[self.player_order])):
			combo = 'Straight'
		elif (is_straight1(self.betting_temp_player_list[self.player_order])):
			combo = 'Straight'
		elif (is_three_of_a_kind(self.betting_temp_player_list[self.player_order])):
			combo = 'Three of a Kind'
		elif (is_two_pair(self.betting_temp_player_list[self.player_order])):
			combo = 'Two Pair'
		elif (is_one_pair(self.betting_temp_player_list[self.player_order])):
			combo = 'One Pair'
		else:
			combo = 'High Card'
		return (l_hand_rankings.index(combo)) * 100
	
	# determine the reward value for a given state
	def determineReward(self, action):
		total_reward = (self.pot - self.betting_temp_player_list[self.player_order]['Money'])
		total_reward -= (self.betting_temp_player_list[self.player_order]['Card1_Weight'] + self.betting_temp_player_list[self.player_order]['Card2_Weight'])
		if (self.betting_temp_player_list[self.player_order]['Card1_Value'] == self.betting_temp_player_list[self.player_order]['Card2_Value']):
			total_reward += (2000 // (13 - l_value_order.index(self.betting_temp_player_list[self.player_order]['Card1_Value'])))
			if (action != 'Fold'):
				total_reward += (100 * self.betting_round)
		else:
			total_reward += (1000 // abs((l_value_order.index(self.betting_temp_player_list[self.player_order]['Card1_Value'])) - l_value_order.index(self.betting_temp_player_list[self.player_order]['Card2_Value'])))
		if (self.betting_temp_player_list[self.player_order]['Card1_Suite'] == self.betting_temp_player_list[self.player_order]['Card2_Suite']):
			total_reward += 500
			value_difference = abs((l_value_order.index(self.betting_temp_player_list[self.player_order]['Card1_Value'])) - l_value_order.index(self.betting_temp_player_list[self.player_order]['Card2_Value']))
			if (value_difference <= 5):
				if (action != 'Fold'):
					total_reward +=  (120 * (1 / self.betting_round))
			else:
				if (action == 'Fold'):
					total_reward += 120 * self.betting_round
		if (action == 'Raise') or (action == 'Fold'):
			total_reward += (100 * self.betting_round)
		if (action == 'Call'):
			total_reward += 500 - (100 * self.betting_round)
		if (self.betting_round == 4):
			total_reward -= self.evaluate_hand()
		return total_reward
		
	# create Q-table matrix
	def createQMatrix(self):
		global q_tables
		for i in range(len(self.betting_temp_player_list)):
			q_tables[0][self.betting_temp_player_list[i]['Name']] = {}
			q_tables[0][self.betting_temp_player_list[i]['Name']]['Raise'] = random.uniform(0, 150)
			q_tables[0][self.betting_temp_player_list[i]['Name']]['Call'] = random.uniform(0, 150)
			q_tables[0][self.betting_temp_player_list[i]['Name']]['Check'] = random.uniform(0, 150)
			q_tables[0][self.betting_temp_player_list[i]['Name']]['Fold'] = random.uniform(0, 150)
			q_tables[1][self.betting_temp_player_list[i]['Name']] = {}
			q_tables[1][self.betting_temp_player_list[i]['Name']]['Raise'] = random.uniform(0, 150)
			q_tables[1][self.betting_temp_player_list[i]['Name']]['Call'] = random.uniform(0, 150)
			q_tables[1][self.betting_temp_player_list[i]['Name']]['Check'] = random.uniform(0, 150)
			q_tables[1][self.betting_temp_player_list[i]['Name']]['Fold'] = random.uniform(0, 150)
			q_tables[2][self.betting_temp_player_list[i]['Name']] = {}
			q_tables[2][self.betting_temp_player_list[i]['Name']]['Raise'] = random.uniform(0, 150)
			q_tables[2][self.betting_temp_player_list[i]['Name']]['Call'] = random.uniform(0, 150)
			q_tables[2][self.betting_temp_player_list[i]['Name']]['Check'] = random.uniform(0, 150)
			q_tables[2][self.betting_temp_player_list[i]['Name']]['Fold'] = random.uniform(0, 150)
			q_tables[3][self.betting_temp_player_list[i]['Name']] = {}
			q_tables[3][self.betting_temp_player_list[i]['Name']]['Raise'] = random.uniform(0, 150)
			q_tables[3][self.betting_temp_player_list[i]['Name']]['Call'] = random.uniform(0, 150)
			q_tables[3][self.betting_temp_player_list[i]['Name']]['Check'] = random.uniform(0, 150)
			q_tables[3][self.betting_temp_player_list[i]['Name']]['Fold'] = random.uniform(0, 150)

	# determine if the current state is a terminal state
	def isTerminal(self):
		if (self.is_round_one):
			last_order = 0
			for num in range(0, len(self.betting_temp_player_list)):
				if not(self.betting_temp_player_list[num]['Folded?']):
					last_order = num
			if (self.last_player_to_raise == '') and (self.player_order == len(self.betting_temp_player_list)):
				return True
			else:
				return False
		else:
			if (self.betting_temp_player_list[self.player_order]['Name'] == self.last_player_to_raise) or (self.last_player_to_raise == ''):
				return True
			else:
				return False

	# choose the next action
	def chooseNextAction(self, epsilon):
		num = random.randint(0, 1000)
		if num / 1000 < epsilon:
			return max(q_tables[self.betting_round - 1][self.current_player], key=q_tables[self.betting_round - 1][self.current_player].get)
		else:
			return random.choice(self.getPossibleActions())

	# adjust action if necessary
	def adjustAction(self, action):
		if action == 'Raise':
			if ((not self.is_round_one) and self.last_player_to_raise != '') or self.all_in:
				action = 'Call'
			if (self.betting_temp_player_list[self.player_order]['Money'] + self.raise_amount > self.betting_temp_player_list[self.player_order]['Balance']):
				action = 'Call'
		if action == 'Call':
			if self.last_player_to_raise == '':
				action = 'Check'
		if action == 'Check':
			if (self.is_round_one and self.player_order != self.big_blind) or (self.last_player_to_raise != ''):
				action = 'Call'
		return action
	
	# perform the action
	def takeAction(self, action):
		if action == 'Raise':
			if ((not self.is_round_one) and self.last_player_to_raise != '') or self.all_in:
				action = 'Call'
		if action == 'Call':
			if self.last_player_to_raise == '':
				action = 'Check'
		if action == 'Check':
			if (self.is_round_one and self.player_order != self.big_blind) or (self.last_player_to_raise != ''):
				action = 'Call'

		if action == 'Raise':
			if self.is_round_one:
				self.last_player_to_raise = self.betting_temp_player_list[self.player_order]['Name']
				self.betting_temp_player_list[self.player_order]['Raised?'] = True
			self.amount_to_match += self.raise_amount
			self.betting_temp_player_list[self.player_order]['Money'] += self.amount_to_match - self.betting_temp_player_list[self.player_order]['Money']
			if self.betting_temp_player_list[self.player_order]['Money'] >= self.betting_temp_player_list[self.player_order]['Balance'] and not self.all_in:
				self.all_in = True
			self.pot += self.betting_temp_player_list[self.player_order]['Money'] - self.betting_temp_player_list[self.player_order]['Money']
		elif action == 'Check':
			self.betting_temp_player_list[self.player_order]['Money'] += 0
		elif action == 'Call':
			self.betting_temp_player_list[self.player_order]['Money'] += self.amount_to_match - self.betting_temp_player_list[self.player_order]['Money']
			if self.betting_temp_player_list[self.player_order]['Money'] >= self.betting_temp_player_list[self.player_order]['Balance'] and not self.all_in:
				self.all_in = True
			self.pot += (self.pot - self.betting_temp_player_list[self.player_order]['Money']) + self.betting_temp_player_list[self.player_order]['Money']
		elif action == 'Fold':
			self.betting_temp_player_list[self.player_order]['Folded?'] = True
			self.folded_players.append(self.betting_temp_player_list[self.player_order]['Name'])
			
	# move to the next player
	def movePlayer(self):
		if (self.player_order) + 1 > len(self.betting_temp_player_list) - 1:
			self.player_order = 0
			self.is_round_one = False
		else:
			self.player_order += 1

		while (self.betting_temp_player_list[self.player_order]['Folded?']):
			if (self.player_order) + 1 > len(self.betting_temp_player_list) - 1:
				self.player_order = 0
				self.is_round_one = False
			else:
				self.player_order += 1
		self.current_player = self.betting_temp_player_list[self.player_order]['Name']

	# training the poker bot
	def training(self):
		global q_tables
		epsilon = 0.8
		discount_factor = 0.9
		learning_rate = 0.9
		for episode in range(1000):
			self.reset()
			while not self.isTerminal():
				action = self.chooseNextAction(epsilon)
				self.takeAction(action)
				action = self.adjustAction(action)
				reward = self.determineReward(action)
				old_q_value = q_tables[self.betting_round - 1][self.current_player][action]
				temporal_difference = reward + (discount_factor * max(q_tables[self.betting_round - 1][self.current_player].values())) - old_q_value
				new_q_value = old_q_value + (learning_rate * temporal_difference)
				q_tables[self.betting_round - 1][self.current_player][action] = new_q_value
				self.movePlayer()
			if (self.is_round_one):
				if self.last_player_to_raise == '' and self.player_order == len(self.betting_temp_player_list):
					action = self.chooseNextAction(epsilon)
					self.takeAction(action)
					action = self.adjustAction(action)
					reward = self.determineReward(action)
					old_q_value = q_tables[self.betting_round - 1][self.current_player][action]
					temporal_difference = reward + (discount_factor * max(q_tables[self.betting_round - 1][self.current_player].values())) - old_q_value
					new_q_value = old_q_value + (learning_rate * temporal_difference)
					q_tables[self.betting_round - 1][self.current_player][action] = new_q_value
					self.movePlayer()

## END ##

#decision_before_flop_pair
def bet11(player,player_type_index):
	global l_matrices
	global low_values_list
	global medium_values_list
	global high_values_list
	actual_choice_index = -1
	if player['Card1_Value'] == player['Card2_Value']:
		if player['Card1_Value'] in low_values_list:
			actual_choice_index = 0
		elif player['Card1_Value'] in medium_values_list:
			actual_choice_index = 1
		elif player['Card1_Value'] in high_values_list:
			actual_choice_index = 2
		player['Function'] = 'Bet11'
		player['Decision'] = l_matrices['decision_before_flop_pair'][player_type_index][actual_choice_index]

#decision_before_flop_in_range_of_straight_flush AND decision_before_flop_same_suite
def bet12_and_bet13(player,player_type_index):
	global l_matrices
	global l_value_order
	global l_value_order1
	actual_choice_index = -1
	if player['Card1_Suite'] == player['Card2_Suite']:
		if player['Card1_Value'] == 'A' or player['Card2_Value'] == 'A':
			if player['Card1_Value'] == 'A':
				if player['Card2_Value'] == '2' or player['Card2_Value'] == '3' or player['Card2_Value'] == '4' or player['Card2_Value'] == '5':
					player['Function'] = 'Bet12'
					actual_choice_index = abs(abs((l_value_order1.index(player['Card1_Value']) + 1) - (l_value_order1.index(player['Card2_Value']) + 1)) - 5)
				elif player['Card2_Value'] == '10' or player['Card2_Value'] == 'J' or player['Card2_Value'] == 'Q' or player['Card2_Value'] == 'K':
					player['Function'] = 'Bet12'
					actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
				else:
					player['Function'] = 'Bet13'
					actual_choice_index = 0
			elif player['Card2_Value'] == 'A':
				if player['Card1_Value'] == '2' or player['Card1_Value'] == '3' or player['Card1_Value'] == '4' or player['Card1_Value'] == '5':
					player['Function'] = 'Bet12'
					actual_choice_index = abs(abs((l_value_order1.index(player['Card1_Value']) + 1) - (l_value_order1.index(player['Card2_Value']) + 1)) - 5)
				elif player['Card1_Value'] == '10' or player['Card1_Value'] == 'J' or player['Card1_Value'] == 'Q' or player['Card1_Value'] == 'K':
					player['Function'] = 'Bet12'
					actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
				else:
					player['Function'] = 'Bet13'
					actual_choice_index = 0
		else:
			if abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) in range(1,5):
				player['Function'] = 'Bet12'
				actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
			elif abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) in range(5,9):
				player['Function'] = 'Bet13'
				actual_choice_index = 0
			elif (abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1))) - 1 in range(9,13):
				player['Function'] = 'Bet13'
				actual_choice_index = 1

	if player['Function'] == 'Bet12':
		player['Decision'] = l_matrices['decision_before_flop_in_range_of_straight_flush'][player_type_index][actual_choice_index]
	elif player['Function'] == 'Bet13':
		player['Decision'] = l_matrices['decision_before_flop_same_suite'][player_type_index][actual_choice_index]

#decision_before_flop_in_range_of_straight
def bet14(player,player_type_index):
	global l_matrices
	global l_value_order
	global l_value_order1
	actual_choice_index = -1
	if player['Card1_Value'] == 'A' or player['Card2_Value'] == 'A':
		if player['Card1_Value'] == 'A':
			if player['Card2_Value'] == '2' or player['Card2_Value'] == '3' or player['Card2_Value'] == '4' or player['Card2_Value'] == '5':
				player['Function'] = 'Bet14'
				actual_choice_index = abs(abs((l_value_order1.index(player['Card1_Value']) + 1) - (l_value_order1.index(player['Card2_Value']) + 1)) - 5)
			elif player['Card2_Value'] == '10' or player['Card2_Value'] == 'J' or player['Card2_Value'] == 'Q' or player['Card2_Value'] == 'K':
				player['Function'] = 'Bet14'
				actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
		elif player['Card2_Value'] == 'A':
			if player['Card1_Value'] == '2' or player['Card1_Value'] == '3' or player['Card1_Value'] == '4' or player['Card1_Value'] == '5':
				player['Function'] = 'Bet14'
				actual_choice_index = abs(abs((l_value_order1.index(player['Card1_Value']) + 1) - (l_value_order1.index(player['Card2_Value']) + 1)) - 5)
			elif player['Card1_Value'] == '10' or player['Card1_Value'] == 'J' or player['Card1_Value'] == 'Q' or player['Card1_Value'] == 'K':
				player['Function'] = 'Bet14'
				actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
	else:
		if abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) in range(1,5):
			player['Function'] = 'Bet14'
			actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)

	if player['Function'] == 'Bet14':
		player['Decision'] = l_matrices['decision_before_flop_in_range_of_straight'][player_type_index][actual_choice_index]

#decision_before_flop_two_distinct_cards
def bet15(player,player_type_index):
	global l_matrices
	global low_values_list
	global medium_values_list
	global high_values_list
	actual_choice_index = -1
	player['Function'] = 'Bet15'
	if (((player['Card1_Value'] in low_values_list) and (player['Card2_Value'] in medium_values_list)) or ((player['Card2_Value'] in low_values_list) and (player['Card1_Value'] in medium_values_list))):
		actual_choice_index = 0
	elif (((player['Card1_Value'] in low_values_list) and (player['Card2_Value'] in high_values_list)) or ((player['Card2_Value'] in low_values_list) and (player['Card1_Value'] in high_values_list))):
		actual_choice_index = 1
	elif (((player['Card1_Value'] in medium_values_list) and (player['Card2_Value'] in high_values_list)) or ((player['Card2_Value'] in medium_values_list) and (player['Card1_Value'] in high_values_list))):
		actual_choice_index = 2
	player['Decision'] = l_matrices['decision_before_flop_two_distinct_cards'][player_type_index][actual_choice_index]

#decision_before_flop_highest_bet_pair
def bet16(player,player_type_index):
	global l_matrices
	global low_values_list
	global medium_values_list
	global high_values_list
	actual_choice_index = -1
	if player['Card1_Value'] == player['Card2_Value']:
		if player['Card1_Value'] in low_values_list:
			actual_choice_index = 0
		elif player['Card1_Value'] in medium_values_list:
			actual_choice_index = 1
		elif player['Card1_Value'] in high_values_list:
			actual_choice_index = 2
		player['Function'] = 'Bet16'
		player['Decision'] = l_matrices['decision_before_flop_highest_bet_pair'][player_type_index][actual_choice_index]

#decision_before_flop_highest_bet_in_range_of_straight_flush AND decision_before_flop_highest_bet_same_suite
def bet17_and_bet18(player,player_type_index):
	global l_matrices
	global l_value_order
	global l_value_order1
	actual_choice_index = -1
	if player['Card1_Suite'] == player['Card2_Suite']:
		if player['Card1_Value'] == 'A' or player['Card2_Value'] == 'A':
			if player['Card1_Value'] == 'A':
				if player['Card2_Value'] == '2' or player['Card2_Value'] == '3' or player['Card2_Value'] == '4' or player['Card2_Value'] == '5':
					player['Function'] = 'Bet17'
					actual_choice_index = abs(abs((l_value_order1.index(player['Card1_Value']) + 1) - (l_value_order1.index(player['Card2_Value']) + 1)) - 5)
				elif player['Card2_Value'] == '10' or player['Card2_Value'] == 'J' or player['Card2_Value'] == 'Q' or player['Card2_Value'] == 'K':
					player['Function'] = 'Bet17'
					actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
				else:
					player['Function'] = 'Bet18'
					actual_choice_index = 0
			elif player['Card2_Value'] == 'A':
				if player['Card1_Value'] == '2' or player['Card1_Value'] == '3' or player['Card1_Value'] == '4' or player['Card1_Value'] == '5':
					player['Function'] = 'Bet17'
					actual_choice_index = abs(abs((l_value_order1.index(player['Card1_Value']) + 1) - (l_value_order1.index(player['Card2_Value']) + 1)) - 5)
				elif player['Card1_Value'] == '10' or player['Card1_Value'] == 'J' or player['Card1_Value'] == 'Q' or player['Card1_Value'] == 'K':
					player['Function'] = 'Bet17'
					actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
				else:
					player['Function'] = 'Bet18'
					actual_choice_index = 0
		else:
			if abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) in range(1,5):
				player['Function'] = 'Bet17'
				actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
			elif abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) in range(5,9):
				player['Function'] = 'Bet18'
				actual_choice_index = 0
			elif (abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1))) - 1 in range(9,13):
				player['Function'] = 'Bet18'
				actual_choice_index = 1

	if player['Function'] == 'Bet17':
		player['Decision'] = l_matrices['decision_before_flop_highest_bet_in_range_of_straight_flush'][player_type_index][actual_choice_index]
	elif player['Function'] == 'Bet18':
		player['Decision'] = l_matrices['decision_before_flop_highest_bet_same_suite'][player_type_index][actual_choice_index]

#decision_before_flop_in_range_of_straight
def bet19(player,player_type_index):
	global l_matrices
	global l_value_order
	global l_value_order1
	actual_choice_index = -1
	if player['Card1_Value'] == 'A' or player['Card2_Value'] == 'A':
		if player['Card1_Value'] == 'A':
			if player['Card2_Value'] == '2' or player['Card2_Value'] == '3' or player['Card2_Value'] == '4' or player['Card2_Value'] == '5':
				player['Function'] = 'Bet19'
				actual_choice_index = abs(abs((l_value_order1.index(player['Card1_Value']) + 1) - (l_value_order1.index(player['Card2_Value']) + 1)) - 5)
			elif player['Card2_Value'] == '10' or player['Card2_Value'] == 'J' or player['Card2_Value'] == 'Q' or player['Card2_Value'] == 'K':
				player['Function'] = 'Bet19'
				actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
		elif player['Card2_Value'] == 'A':
			if player['Card1_Value'] == '2' or player['Card1_Value'] == '3' or player['Card1_Value'] == '4' or player['Card1_Value'] == '5':
				player['Function'] = 'Bet19'
				actual_choice_index = abs(abs((l_value_order1.index(player['Card1_Value']) + 1) - (l_value_order1.index(player['Card2_Value']) + 1)) - 5)
			elif player['Card1_Value'] == '10' or player['Card1_Value'] == 'J' or player['Card1_Value'] == 'Q' or player['Card1_Value'] == 'K':
				player['Function'] = 'Bet19'
				actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)
	else:
		if abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) in range(1,5):
			player['Function'] = 'Bet19'
			actual_choice_index = abs(abs((l_value_order.index(player['Card1_Value']) + 1) - (l_value_order.index(player['Card2_Value']) + 1)) - 5)

	if player['Function'] == 'Bet19':
		player['Decision'] = l_matrices['decision_before_flop_highest_bet_in_range_of_straight'][player_type_index][actual_choice_index]

#decision_before_flop_two_distinct_cards
def bet110(player,player_type_index):
	global l_matrices
	global low_values_list
	global medium_values_list
	global high_values_list
	actual_choice_index = -1
	player['Function'] = 'Bet110'
	if (((player['Card1_Value'] in low_values_list) and (player['Card2_Value'] in medium_values_list)) or ((player['Card2_Value'] in low_values_list) and (player['Card1_Value'] in medium_values_list))):
		actual_choice_index = 0
	elif (((player['Card1_Value'] in low_values_list) and (player['Card2_Value'] in high_values_list)) or ((player['Card2_Value'] in low_values_list) and (player['Card1_Value'] in high_values_list))):
		actual_choice_index = 1
	elif (((player['Card1_Value'] in medium_values_list) and (player['Card2_Value'] in high_values_list)) or ((player['Card2_Value'] in medium_values_list) and (player['Card1_Value'] in high_values_list))):
		actual_choice_index = 2
	player['Decision'] = l_matrices['decision_before_flop_highest_bet_two_distinct_cards'][player_type_index][actual_choice_index]

#first round of betting (pre-flop)
def bet1(first_hand_yes):
	global betting_temp_player_list
	global high_values_list
	global medium_values_list
	global low_values_list
	global raise_amount
	global big_blind_amount
	global small_blind_amount
	global big_blind
	global small_blind
	global q_tables
	matrix_name = ''
	player_type_index = 0
	last_player_to_raise = ''
	all_in = False
	amount_to_match = big_blind_amount
	highest_bet = False
	previous_raise_amount = 0
	player_who_put_all_in = ''
	return_list = []
	extra_money = []
	extra_money_value = 0
	skip_betting = False
	one_player_left = False
	count = 0
	first_hand_yes = first_hand_yes
	index_count = 0
	active_player_count = 0

	for player in betting_temp_player_list:
		extra_money.append(0)

	count = 0
	for player in betting_temp_player_list:
		if one_player_left == True:
			break
		else:
			player_type_index = determine_player_type_indexes(player)
			active_player_count = 0
			if player['Player_Type'] != 'Human':
				QLearningState = Q_Learning(player['Name'], 1, True, last_player_to_raise, amount_to_match, betting_temp_player_list.index(player), False)
				if first_hand_yes:
					QLearningState.createQMatrix()
				QLearningState.training()

				player['Decision'] = max(q_tables[0][player['Name']], key=q_tables[0][player['Name']].get)

			return_list = bet(player,amount_to_match,last_player_to_raise,highest_bet,True,True,first_hand_yes,1)
			amount_to_match = return_list[0]
			last_player_to_raise = return_list[1]

			if return_list[2] > 0:
				extra_money[index_count] = return_list[2]

			for player in betting_temp_player_list:
				if player['Folded?'] != True:
					active_player_count += 1

			if active_player_count == 1:
				one_player_left = True
					
		index_count += 1

	#run through player second time until last player to raise
	index_count = 0
	player_type_index = determine_player_type_indexes(player)
	for player in betting_temp_player_list:
		if one_player_left == True:
			break
		else:
			if player['Folded?'] == False:
				if last_player_to_raise == '':
					break
				else:
					player_type_index = determine_player_type_indexes(player)
					active_player_count = 0
					if player['Name'] == last_player_to_raise:
						break
					else:
						if player['Player_Type'] != 'Human':
							QLearningState = Q_Learning(player['Name'], 1, False, last_player_to_raise, amount_to_match, betting_temp_player_list.index(player), False)
							QLearningState.training()

							player['Decision'] = max(q_tables[0][player['Name']], key=q_tables[0][player['Name']].get)

				return_list = bet(player,amount_to_match,last_player_to_raise,True,True,False,first_hand_yes,1)
				amount_to_match = return_list[0]
				last_player_to_raise = return_list[1]

				if return_list[2] > 0:
					extra_money[index_count] = return_list[2]

				for player in betting_temp_player_list:
					if player['Folded?'] != True:
						active_player_count += 1

				if active_player_count == 1:
					one_player_left = True

		index_count += 1

	skip_betting = redistribute_money(extra_money,skip_betting,last_player_to_raise)
	return [skip_betting,one_player_left]

#decision_before_turn_royal_flush
def bet21(player,player_type_index,card_count):
	global community_cards
	global l_matrices
	global high_values_list
	global l_suite_order
	actual_choice_index = -1
	not_in_range = False
	count_cards = 1
	local_card_list = []
	possible_index_combos = [[0,1,2,3,4]]
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])
	for combo in possible_index_combos:
		if local_card_list[combo[0]]['Suite'] == local_card_list[combo[1]]['Suite'] == local_card_list[combo[2]]['Suite'] == local_card_list[combo[3]]['Suite'] == local_card_list[combo[4]]['Suite']:
			for num in combo:
				if local_card_list[num]['Value'] not in high_values_list:
					not_in_range = True
					break
			if not not_in_range:
				player['Function'] = 'Bet21'
				actual_choice_index = l_suite_order.index(player['Card1_Suite'])
				player['Decision'] = l_matrices['decision_before_turn_royal_flush'][player_type_index][actual_choice_index]
				break

#decision_before_turn_straight_flush
def bet22(player,player_type_index,card_count):
	global l_matrices
	global low_values_list1
	global medium_values_list
	global high_values_list
	global l_suite_order
	global community_cards
	count = 0
	count_cards = 1
	count1 = 0
	actual_choice_index = -1
	possible_index_combos = [[0,1,2,3,4]]
	local_card_list = []
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value'], 'Number' : community_cards[count_cards - 3]['Number']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value'], 'Number' : player['Card1_Number']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value'], 'Number' : player['Card2_Number']})
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])
	for combo in possible_index_combos:
		if local_card_list[combo[0]]['Suite'] == local_card_list[combo[1]]['Suite'] == local_card_list[combo[2]]['Suite'] == local_card_list[combo[3]]['Suite'] == local_card_list[combo[4]]['Suite']:
			low_card = local_card_list[combo[0]]
			high_card = low_card
			for num in combo:
				if int(local_card_list[num]['Number']) < int(low_card['Number']):
					low_card = local_card_list[num]
			for num in combo:
				if int(local_card_list[num]['Number']) > int(high_card['Number']):
					high_card = local_card_list[num]
			for num in combo:
				if local_card_list[num]['Number'] in range(int(low_card['Number']), int(low_card['Number']) + 5):
					count += 1
			if count == 5:
				player['Function'] = 'Bet22'
				actual_choice_index = l_suite_order.index(local_card_list[0]['Suite'])
				if high_card['Value'] in high_values_list:
					actual_choice_index *= 3
				elif high_card['Value'] in medium_values_list:
					actual_choice_index = (actual_choice_index * 3) + 1
				elif high_card['Value'] in low_values_list1:
					actual_choice_index = (actual_choice_index * 3) + 2
				player['Decision'] = l_matrices['decision_before_turn_straight_flush'][player_type_index][actual_choice_index]

#decision_before_turn_four_of_a_kind AND decision_before_turn_full_house
def bet23_and_bet24(player,player_type_index,card_count):
	global l_matrices
	global low_values_list
	global medium_values_list
	global high_values_list
	global community_cards
	actual_choice_index = -1
	count_cards = 1
	possible_index_combos = [[0,1,2,3,4]]
	possible_index_combos_four_of_a_kind = [[0,1,2,3],[0,1,2,4],[0,1,3,4],[0,2,3,4],[1,2,3,4]]
	possible_index_combos_full_house = [[0,1,2,3,4],[0,1,3,2,4],[0,1,4,2,3],[0,2,3,1,4],[0,2,4,1,3],[0,3,4,1,2],[1,2,3,0,4],[1,2,4,0,3],[1,3,4,0,2],[2,3,4,0,1]]
	local_card_list = []
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append(community_cards[count_cards - 3]['Value'])
		else:
			if count_cards == 1:
				local_card_list.append(player['Card1_Value'])
			else:
				local_card_list.append(player['Card2_Value'])
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])
	for combo in possible_index_combos:
		for index_combo in possible_index_combos_four_of_a_kind:
			if local_card_list[combo[index_combo[0]]] == local_card_list[combo[index_combo[1]]] == local_card_list[combo[index_combo[2]]] == local_card_list[combo[index_combo[3]]]:
				player['Function'] = 'Bet23'
				if local_card_list[combo[index_combo[0]]] in high_values_list:
					actual_choice_index = 0
				elif local_card_list[combo[index_combo[0]]] in medium_values_list:
					actual_choice_index = 1
				elif local_card_list[combo[index_combo[0]]] in low_values_list:
					actual_choice_index = 2
				player['Decision'] = l_matrices['decision_before_turn_four_of_a_kind'][player_type_index][actual_choice_index]
		if player['Decision'] == '':
			for index_combo in possible_index_combos_full_house:
				if local_card_list[combo[index_combo[0]]] == local_card_list[combo[index_combo[1]]] == local_card_list[combo[index_combo[2]]] and local_card_list[combo[index_combo[3]]] == local_card_list[combo[index_combo[4]]] and local_card_list[combo[index_combo[0]]] != local_card_list[combo[index_combo[3]]]:
					player['Function'] = 'Bet24'
					if local_card_list[combo[index_combo[0]]] in high_values_list:
						actual_choice_index = 0
					elif local_card_list[combo[index_combo[0]]] in medium_values_list:
						actual_choice_index = 1
					elif local_card_list[combo[index_combo[0]]] in low_values_list:
						actual_choice_index = 2
					player['Decision'] = l_matrices['decision_before_turn_full_house'][player_type_index][actual_choice_index]

#decision_before_turn_flush
def bet25(player,player_type_index,card_count):
	global l_matrices
	global l_suite_order
	global l_value_order
	global low_values_list
	global medium_values_list
	global high_values_list
	global community_cards
	card_suite_list = [0,0,0,0]
	count_cards = 1
	local_card_list = []
	possible_index_combos = [[0,1,2,3,4]]
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])
	highest_card = local_card_list[0]
	for combo in possible_index_combos:
		if local_card_list[combo[0]]['Suite'] == local_card_list[combo[1]]['Suite'] == local_card_list[combo[2]]['Suite'] == local_card_list[combo[3]]['Suite'] == local_card_list[combo[4]]['Suite']:
			for num in combo:
				if l_value_order.index(local_card_list[num]['Value']) > l_value_order.index(highest_card['Value']):
					highest_card = local_card_list[num]
			player['Function'] = 'Bet25'
			actual_choice_index = l_suite_order.index(highest_card['Suite'])
			if highest_card['Value'] in high_values_list:
				actual_choice_index *= 3
			elif highest_card['Value'] in medium_values_list:
				actual_choice_index = (actual_choice_index * 3) + 1
			elif highest_card['Value'] in low_values_list1:
				actual_choice_index = (actual_choice_index * 3) + 2
			player['Decision'] = l_matrices['decision_before_turn_flush'][player_type_index][actual_choice_index]
			break

#decision_before_turn_straight
def bet26(player,player_type_index,card_count):
	global l_matrices
	global l_suite_order
	global low_values_list
	global medium_values_list
	global high_values_list
	global community_cards
	global l_value_order
	global l_value_order1
	count = 0
	actual_choice_index = -1
	count_cards = 1
	local_card_list = []
	possible_index_combos = [[0,1,2,3,4]]
	values_evaluated = []

	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])

	lowest_card = local_card_list[0]
	highest_card = lowest_card
	
	for combo in possible_index_combos:
		for num in combo:
			if l_value_order.index(local_card_list[num]['Value']) < l_value_order.index(lowest_card['Value']):
				lowest_card = local_card_list[num]

		for num in combo:
			if (local_card_list[num]['Value'] not in values_evaluated) and (l_value_order.index(local_card_list[num]['Value']) in range(l_value_order.index(lowest_card['Value']),l_value_order.index(lowest_card['Value']) + 5)):
				values_evaluated.append(local_card_list[num]['Value'])
				count += 1

		if count == 5:
			player['Function'] = 'Bet26'

			for num in combo:
				if l_value_order.index(local_card_list[num]['Value']) > l_value_order.index(highest_card['Value']):
					highest_card = local_card_list[num]

			actual_choice_index = l_suite_order.index(highest_card['Suite'])
			if highest_card['Value'] in high_values_list:
				actual_choice_index *= 3
			elif highest_card['Value'] in medium_values_list:
				actual_choice_index = (actual_choice_index * 3) + 1
			elif highest_card['Value'] in low_values_list1:
				actual_choice_index = (actual_choice_index * 3) + 2
			player['Decision'] = l_matrices['decision_before_turn_straight'][player_type_index][actual_choice_index]
		else:
			values_evaluated = []
			count = 0

			for num in combo:
				if l_value_order1.index(local_card_list[num]['Value']) < l_value_order1.index(lowest_card['Value']):
					lowest_card = local_card_list[num]

			for num in combo:
				if (local_card_list[num]['Value'] not in values_evaluated) and (l_value_order1.index(local_card_list[num]['Value']) in range(l_value_order1.index(lowest_card['Value']),l_value_order1.index(lowest_card['Value']) + 5)):
					values_evaluated.append(local_card_list[num]['Value'])
					count += 1

			for num in combo:
				if l_value_order1.index(local_card_list[num]['Value']) > l_value_order1.index(highest_card['Value']):
					highest_card = local_card_list[num]

			if count == 5:
				player['Function'] = 'Bet26'
				actual_choice_index = l_suite_order.index(highest_card['Suite'])
				if highest_card['Value'] in high_values_list:
					actual_choice_index *= 3
				elif highest_card['Value'] in medium_values_list:
					actual_choice_index = (actual_choice_index * 3) + 1
				elif highest_card['Value'] in low_values_list1:
					actual_choice_index = (actual_choice_index * 3) + 2
				player['Decision'] = l_matrices['decision_before_turn_straight'][player_type_index][actual_choice_index]

#decision_before_turn_three_of_a_kind AND decision_before_turn_two_pair AND decision_before_turn_one_pair
def bet27_and_bet28_and_bet29(player,player_type_index,card_count):
	global l_matrices
	global community_cards
	global l_value_order
	global high_values_list
	global medium_values_list
	global low_values_list
	local_card_list = []
	actual_choice_index = -1
	pair_value_list = []
	possible_index_combos = []
	value_index = 0
	count_cards = 1
	value_count_list = [0,0,0,0,0,0,0,0,0,0,0,0,0]
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append(community_cards[count_cards - 3]['Value'])
		else:
			if count_cards == 1:
				local_card_list.append(player['Card1_Value'])
			else:
				local_card_list.append(player['Card2_Value'])
		count_cards += 1
	for value in local_card_list:
		value_count_list[l_value_order.index(value)] += 1
	for value in value_count_list:
		if value == 3:
			player['Function'] = 'Bet27'
			if l_value_order[value_index] in high_values_list:
				actual_choice_index = 0
			elif l_value_order[value_index] in medium_values_list:
				actual_choice_index = 1
			elif l_value_order[value_index] in low_values_list:
				actual_choice_index = 2
			player['Decision'] = l_matrices['decision_before_turn_three_of_a_kind'][player_type_index][actual_choice_index]
			break
		value_index += 1
	if player['Decision'] == '':
		for value in value_count_list:
			if value == 2:
				pair_value_list.append(value)
		if len(pair_value_list) == 2:
			player['Function'] = 'Bet28'
			if pair_value_list[0] in high_values_list and pair_value_list[1] in high_values_list:
				actual_choice_index = 0
			elif (pair_value_list[0] in high_values_list and pair_value_list[1] in medium_values_list) or (pair_value_list[0] in medium_values_list and pair_value_list[1] in high_values_list):
				actual_choice_index = 1
			elif (pair_value_list[0] in high_values_list and pair_value_list[1] in low_values_list) or (pair_value_list[0] in low_values_list and pair_value_list[1] in high_values_list): 
				actual_choice_index = 2
			elif pair_value_list[0] in medium_values_list and pair_value_list[1] in medium_values_list:
				actual_choice_index = 3
			elif (pair_value_list[0] in medium_values_list and pair_value_list[1] in low_values_list) or (pair_value_list[0] in low_values_list and pair_value_list[1] in medium_values_list):
				actual_choice_index = 4
			elif pair_value_list[0] in low_values_list and pair_value_list[1] in low_values_list:
				actual_choice_index = 5
			player['Decision'] = l_matrices['decision_before_turn_two_pair'][player_type_index][actual_choice_index]
		elif len(pair_value_list) == 1:
			player['Function'] = 'Bet29'
			if pair_value_list[0] in high_values_list:
				actual_choice_index = 0
			elif pair_value_list[0] in medium_values_list:
				actual_choice_index = 1
			elif pair_value_list[0] in low_values_list:
				actual_choice_index = 2
			player['Decision'] = l_matrices['decision_before_turn_one_pair'][player_type_index][actual_choice_index]
	
#decision_before_turn_in_range_of_royal_flush AND decision_before_turn_in_range_of_straight_flush AND decision_before_turn_in_range_of_royal_flush_and_straight_flush
def bet210_and_bet211_and_bet212(player,player_type_index,card_count):
	global community_cards
	global l_matrices
	global l_value_order1
	global l_suite_order
	actual_choice_index = -1
	local_card_list = []
	card_suite_list = [0,0,0,0]
	suite_to_be_checked = ''
	cards_to_check_list = []
	count_cards = 1
	values_list = []
	checkable_suites = []
	low_value = ''
	count = 0
	count1 = 0
	ace_there = False
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	for card in local_card_list:
		card_suite_list[l_suite_order.index(card['Suite'])] += 1
	for num in card_suite_list:
		if num >= 3:
			checkable_suites.append(l_suite_order[count])
			break
		count += 1
	count = 0
	if checkable_suites != []:
		for suite_to_be_checked in checkable_suites:
			for card in local_card_list:
				if card['Suite'] == suite_to_be_checked:
					cards_to_check_list.append(card)
					values_list.append(card['Value'])
			for value in values_list:
				if value == '10' or value == 'J' or value == 'Q' or value == 'K' or value == 'A':
					count += 1
			for value in values_list:
				if value == 'A' and count >= 3:
					ace_there = True
					player['Function'] = 'Bet210'
					actual_choice_index = count - 3
					player['Decision'] = l_matrices['decision_before_turn_in_range_of_royal_flush'][player_type_index][actual_choice_index]
					break

			low_value = 'K'
			for value in values_list:
				if player['Decision'] != '':
					break
				else:
					low_value = value
					for value in values_list:
						if l_value_order1.index(value) in range(l_value_order1.index(low_value), l_value_order1.index(low_value) + 5):
							count1 += 1
					if count1 >= 3 and count < 3:
						player['Function'] = 'Bet211'
						actual_choice_index = l_suite_order.index(cards_to_check_list[0]['Suite'])
						player['Decision'] = l_matrices['decision_before_turn_in_range_of_straight_flush'][player_type_index][actual_choice_index]
					elif (not ace_there) and (count >= 3):
						player['Function'] = 'Bet212'
						actual_choice_index = count - 3
						player['Decision'] = l_matrices['decision_before_turn_in_range_of_royal_flush_and_straight_flush'][player_type_index][actual_choice_index]

#decision_before_turn_in_range_of_flush
def bet213(player,player_type_index,card_count):
	global l_matrices
	global l_suite_order
	global community_cards
	card_suite_list = [0,0,0,0]
	local_card_list = []
	count_cards = 1
	actual_choice_index = -1
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append(community_cards[count_cards - 3]['Suite'])
		else:
			if count_cards == 1:
				local_card_list.append(player['Card1_Suite'])
			else:
				local_card_list.append(player['Card2_Suite'])
		count_cards += 1
	for suite in local_card_list:
		card_suite_list[l_suite_order.index(suite)] += 1
	for num in card_suite_list:
		if num >= 3:
			player['Function'] = 'Bet213'
			actual_choice_index = card_suite_list.index(num)
			player['Decision'] = l_matrices['decision_before_turn_in_range_of_flush'][player_type_index][actual_choice_index]
			break

#decision_before_turn_in_range_of_straight
def bet214(player,player_type_index,card_count):
	global l_matrices
	global community_cards
	global l_value_order
	global l_value_order1
	local_card_list = []
	count_cards = 1
	actual_choice_index = -1
	lowest_card = {}
	count = 0
	in_range_cards_count = 0
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	lowest_card = local_card_list[0]
	for card in local_card_list:
		count = 0
		lowest_card = card
		for card1 in local_card_list:
			if l_value_order.index(card1['Value']) in range(l_value_order.index(lowest_card['Value']),l_value_order.index(lowest_card['Value']) + 5):
				count += 1
		if (count >= 3) and (count > in_range_cards_count):
			player['Function'] = 'Bet214'
			actual_choice_index = count - 3
			player['Decision'] = l_matrices['decision_before_turn_in_range_of_straight'][player_type_index][actual_choice_index]

	if player['Decision'] == '':
		count = 0
		in_range_cards_count = 0
		for card in local_card_list:
			count = 0
			lowest_card = card
			for card1 in local_card_list:
				if l_value_order1.index(card1['Value']) in range(l_value_order1.index(lowest_card['Value']),l_value_order1.index(lowest_card['Value']) + 5):
					count += 1
			if (count >= 3) and (count > in_range_cards_count):
				player['Function'] = 'Bet214'
				actual_choice_index = count - 3
				player['Decision'] = l_matrices['decision_before_turn_in_range_of_straight'][player_type_index][actual_choice_index]

#decision_before_turn_all_distinct_cards
def bet215(player,player_type_index,card_count):
	global l_matrices
	global low_values_list
	global medium_values_list
	global high_values_list
	global l_value_order
	global l_suite_order
	local_card_list = []
	actual_choice_index = -1
	count_cards = 1
	highest_card = {}
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Value' : community_cards[count_cards - 3]['Value'], 'Suite' : community_cards[count_cards - 3]['Suite']})
		else:
			if count_cards == 1:
				local_card_list.append({'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite']})
			else:
				local_card_list.append({'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite']})
		count_cards += 1
	highest_card = local_card_list[0]
	for card in local_card_list:
		if l_value_order.index(card['Value']) > l_value_order.index(highest_card['Value']):
			highest_card = card
	player['Function'] = 'Bet215'
	actual_choice_index = l_suite_order.index(highest_card['Suite'])
	if highest_card['Value'] in high_values_list:
		actual_choice_index *= 3
	elif highest_card['Value'] in medium_values_list:
		actual_choice_index = (actual_choice_index * 3) + 1
	elif highest_card['Value'] in low_values_list1:
		actual_choice_index = (actual_choice_index * 3) + 2
	player['Decision'] = l_matrices['decision_before_turn_all_distinct_cards'][player_type_index][actual_choice_index]

#decision_before_turn_highest_bet_royal_flush
def bet216(player,player_type_index,card_count):
	global community_cards
	global l_matrices
	global high_values_list
	global l_suite_order
	actual_choice_index = -1
	not_in_range = False
	count_cards = 1
	local_card_list = []
	possible_index_combos = [[0,1,2,3,4]]
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])
	for combo in possible_index_combos:
		if local_card_list[combo[0]]['Suite'] == local_card_list[combo[1]]['Suite'] == local_card_list[combo[2]]['Suite'] == local_card_list[combo[3]]['Suite'] == local_card_list[combo[4]]['Suite']:
			for num in combo:
				if local_card_list[num]['Value'] not in high_values_list:
					not_in_range = True
					break
			if not not_in_range:
				player['Function'] = 'Bet216'
				actual_choice_index = l_suite_order.index(player['Card1_Suite'])
				player['Decision'] = l_matrices['decision_before_turn_highest_bet_royal_flush'][player_type_index][actual_choice_index]
				break

#decision_before_turn_highest_bet_straight_flush
def bet217(player,player_type_index,card_count):
	global l_matrices
	global low_values_list1
	global medium_values_list
	global high_values_list
	global l_suite_order
	global community_cards
	count = 0
	count_cards = 1
	count1 = 0
	actual_choice_index = -1
	possible_index_combos = [[0,1,2,3,4]]
	local_card_list = []
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value'], 'Number' : community_cards[count_cards - 3]['Number']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value'], 'Number' : player['Card1_Number']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value'], 'Number' : player['Card2_Number']})
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])
	for combo in possible_index_combos:
		if local_card_list[combo[0]]['Suite'] == local_card_list[combo[1]]['Suite'] == local_card_list[combo[2]]['Suite'] == local_card_list[combo[3]]['Suite'] == local_card_list[combo[4]]['Suite']:
			low_card = local_card_list[combo[0]]
			high_card = low_card
			for num in combo:
				if int(local_card_list[num]['Number']) < int(low_card['Number']):
					low_card = local_card_list[num]
			for num in combo:
				if int(local_card_list[num]['Number']) > int(high_card['Number']):
					high_card = local_card_list[num]
			for num in combo:
				if local_card_list[num]['Number'] in range(int(low_card['Number']), int(low_card['Number']) + 5):
					count += 1
			if count == 5:
				player['Function'] = 'Bet217'
				actual_choice_index = l_suite_order.index(local_card_list[0]['Suite'])
				if high_card['Value'] in high_values_list:
					actual_choice_index *= 3
				elif high_card['Value'] in medium_values_list:
					actual_choice_index = (actual_choice_index * 3) + 1
				elif high_card['Value'] in low_values_list1:
					actual_choice_index = (actual_choice_index * 3) + 2
				player['Decision'] = l_matrices['decision_before_turn_highest_bet_straight_flush'][player_type_index][actual_choice_index]

#decision_before_turn_highest_bet_four_of_a_kind AND decision_before_turn_highest_bet_full_house
def bet218_and_bet219(player,player_type_index,card_count):
	global l_matrices
	global low_values_list
	global medium_values_list
	global high_values_list
	global community_cards
	actual_choice_index = -1
	count_cards = 1
	possible_index_combos = [[0,1,2,3,4]]
	possible_index_combos_four_of_a_kind = [[0,1,2,3],[0,1,2,4],[0,1,3,4],[0,2,3,4],[1,2,3,4]]
	possible_index_combos_full_house = [[0,1,2,3,4],[0,1,3,2,4],[0,1,4,2,3],[0,2,3,1,4],[0,2,4,1,3],[0,3,4,1,2],[1,2,3,0,4],[1,2,4,0,3],[1,3,4,0,2],[2,3,4,0,1]]
	local_card_list = []
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append(community_cards[count_cards - 3]['Value'])
		else:
			if count_cards == 1:
				local_card_list.append(player['Card1_Value'])
			else:
				local_card_list.append(player['Card2_Value'])
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])
	for combo in possible_index_combos:
		for index_combo in possible_index_combos_four_of_a_kind:
			if local_card_list[combo[index_combo[0]]] == local_card_list[combo[index_combo[1]]] == local_card_list[combo[index_combo[2]]] == local_card_list[combo[index_combo[3]]]:
				player['Function'] = 'Bet218'
				if local_card_list[combo[index_combo[0]]] in high_values_list:
					actual_choice_index = 0
				elif local_card_list[combo[index_combo[0]]] in medium_values_list:
					actual_choice_index = 1
				elif local_card_list[combo[index_combo[0]]] in low_values_list:
					actual_choice_index = 2
				player['Decision'] = l_matrices['decision_before_turn_highest_bet_four_of_a_kind'][player_type_index][actual_choice_index]
		if player['Decision'] == '':
			for index_combo in possible_index_combos_full_house:
				if local_card_list[combo[index_combo[0]]] == local_card_list[combo[index_combo[1]]] == local_card_list[combo[index_combo[2]]] and local_card_list[combo[index_combo[3]]] == local_card_list[combo[index_combo[4]]] and local_card_list[combo[index_combo[0]]] != local_card_list[combo[index_combo[3]]]:
					player['Function'] = 'Bet219'
					if local_card_list[combo[index_combo[0]]] in high_values_list:
						actual_choice_index = 0
					elif local_card_list[combo[index_combo[0]]] in medium_values_list:
						actual_choice_index = 1
					elif local_card_list[combo[index_combo[0]]] in low_values_list:
						actual_choice_index = 2
					player['Decision'] = l_matrices['decision_before_turn_highest_bet_full_house'][player_type_index][actual_choice_index]

#decision_before_turn_highest_bet_flush
def bet220(player,player_type_index,card_count):
	global l_matrices
	global l_suite_order
	global l_value_order
	global low_values_list
	global medium_values_list
	global high_values_list
	global community_cards
	card_suite_list = [0,0,0,0]
	count_cards = 1
	local_card_list = []
	possible_index_combos = [[0,1,2,3,4]]
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])
	highest_card = local_card_list[0]
	for combo in possible_index_combos:
		if local_card_list[combo[0]]['Suite'] == local_card_list[combo[1]]['Suite'] == local_card_list[combo[2]]['Suite'] == local_card_list[combo[3]]['Suite'] == local_card_list[combo[4]]['Suite']:
			for num in combo:
				if l_value_order.index(local_card_list[num]['Value']) > l_value_order.index(highest_card['Value']):
					highest_card = local_card_list[num]
			player['Function'] = 'Bet220'
			actual_choice_index = l_suite_order.index(highest_card['Suite'])
			if highest_card['Value'] in high_values_list:
				actual_choice_index *= 3
			elif highest_card['Value'] in medium_values_list:
				actual_choice_index = (actual_choice_index * 3) + 1
			elif highest_card['Value'] in low_values_list1:
				actual_choice_index = (actual_choice_index * 3) + 2
			player['Decision'] = l_matrices['decision_before_turn_highest_bet_flush'][player_type_index][actual_choice_index]
			break

#decision_before_turn_highest_bet_straight
def bet221(player,player_type_index,card_count):
	global l_matrices
	global l_suite_order
	global low_values_list
	global medium_values_list
	global high_values_list
	global community_cards
	global l_value_order
	global l_value_order1
	count = 0
	actual_choice_index = -1
	count_cards = 1
	local_card_list = []
	possible_index_combos = [[0,1,2,3,4]]
	values_evaluated = []

	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	if card_count == 6:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([1,2,3,4,5])
	elif card_count == 7:
		possible_index_combos.append([0,1,2,3,5])
		possible_index_combos.append([0,1,2,3,6])
		possible_index_combos.append([0,1,2,4,5])
		possible_index_combos.append([0,1,2,4,6])
		possible_index_combos.append([0,1,2,5,6])
		possible_index_combos.append([0,1,3,4,5])
		possible_index_combos.append([0,1,3,4,6])
		possible_index_combos.append([0,1,3,5,6])
		possible_index_combos.append([0,1,4,5,6])
		possible_index_combos.append([0,2,3,4,5])
		possible_index_combos.append([0,2,3,4,6])
		possible_index_combos.append([0,2,3,5,6])
		possible_index_combos.append([0,2,4,5,6])
		possible_index_combos.append([0,3,4,5,6])
		possible_index_combos.append([1,2,3,4,5])
		possible_index_combos.append([1,2,3,4,6])
		possible_index_combos.append([1,2,3,5,6])
		possible_index_combos.append([1,2,4,5,6])
		possible_index_combos.append([1,3,4,5,6])
		possible_index_combos.append([2,3,4,5,6])

	lowest_card = local_card_list[0]
	highest_card = lowest_card
	
	for combo in possible_index_combos:
		for num in combo:
			if l_value_order.index(local_card_list[num]['Value']) < l_value_order.index(lowest_card['Value']):
				lowest_card = local_card_list[num]

		for num in combo:
			if (local_card_list[num]['Value'] not in values_evaluated) and (l_value_order.index(local_card_list[num]['Value']) in range(l_value_order.index(lowest_card['Value']),l_value_order.index(lowest_card['Value']) + 5)):
				values_evaluated.append(local_card_list[num]['Value'])
				count += 1

		if count == 5:
			player['Function'] = 'Bet221'

			for num in combo:
				if l_value_order.index(local_card_list[num]['Value']) > l_value_order.index(highest_card['Value']):
					highest_card = local_card_list[num]

			actual_choice_index = l_suite_order.index(highest_card['Suite'])
			if highest_card['Value'] in high_values_list:
				actual_choice_index *= 3
			elif highest_card['Value'] in medium_values_list:
				actual_choice_index = (actual_choice_index * 3) + 1
			elif highest_card['Value'] in low_values_list1:
				actual_choice_index = (actual_choice_index * 3) + 2
			player['Decision'] = l_matrices['decision_before_turn_highest_bet_straight'][player_type_index][actual_choice_index]
		else:
			values_evaluated = []
			count = 0

			for num in combo:
				if l_value_order1.index(local_card_list[num]['Value']) < l_value_order1.index(lowest_card['Value']):
					lowest_card = local_card_list[num]

			for num in combo:
				if (local_card_list[num]['Value'] not in values_evaluated) and (l_value_order1.index(local_card_list[num]['Value']) in range(l_value_order1.index(lowest_card['Value']),l_value_order1.index(lowest_card['Value']) + 5)):
					values_evaluated.append(local_card_list[num]['Value'])
					count += 1

			for num in combo:
				if l_value_order1.index(local_card_list[num]['Value']) > l_value_order1.index(highest_card['Value']):
					highest_card = local_card_list[num]

			if count == 5:
				player['Function'] = 'Bet221'
				actual_choice_index = l_suite_order.index(highest_card['Suite'])
				if highest_card['Value'] in high_values_list:
					actual_choice_index *= 3
				elif highest_card['Value'] in medium_values_list:
					actual_choice_index = (actual_choice_index * 3) + 1
				elif highest_card['Value'] in low_values_list1:
					actual_choice_index = (actual_choice_index * 3) + 2
				player['Decision'] = l_matrices['decision_before_turn_straight'][player_type_index][actual_choice_index]

#decision_before_turn_highest_bet_three_of_a_kind AND decision_before_turn_highest_bet_two_pair AND decision_before_turn_highest_bet_one_pair
def bet222_and_bet223_and_bet224(player,player_type_index,card_count):
	global l_matrices
	global community_cards
	global l_value_order
	global high_values_list
	global medium_values_list
	global low_values_list
	local_card_list = []
	actual_choice_index = -1
	pair_value_list = []
	possible_index_combos = []
	value_index = 0
	count_cards = 1
	value_count_list = [0,0,0,0,0,0,0,0,0,0,0,0,0]
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append(community_cards[count_cards - 3]['Value'])
		else:
			if count_cards == 1:
				local_card_list.append(player['Card1_Value'])
			else:
				local_card_list.append(player['Card2_Value'])
		count_cards += 1
	for value in local_card_list:
		value_count_list[l_value_order.index(value)] += 1
	for value in value_count_list:
		if value == 3:
			player['Function'] = 'Bet222'
			if l_value_order[value_index] in high_values_list:
				actual_choice_index = 0
			elif l_value_order[value_index] in medium_values_list:
				actual_choice_index = 1
			elif l_value_order[value_index] in low_values_list:
				actual_choice_index = 2
			player['Decision'] = l_matrices['decision_before_turn_highest_bet_three_of_a_kind'][player_type_index][actual_choice_index]
			break
		value_index += 1
	if player['Decision'] == '':
		for value in value_count_list:
			if value == 2:
				pair_value_list.append(value)
		if len(pair_value_list) == 2:
			player['Function'] = 'Bet223'
			if pair_value_list[0] in high_values_list and pair_value_list[1] in high_values_list:
				actual_choice_index = 0
			elif (pair_value_list[0] in high_values_list and pair_value_list[1] in medium_values_list) or (pair_value_list[0] in medium_values_list and pair_value_list[1] in high_values_list):
				actual_choice_index = 1
			elif (pair_value_list[0] in high_values_list and pair_value_list[1] in low_values_list) or (pair_value_list[0] in low_values_list and pair_value_list[1] in high_values_list): 
				actual_choice_index = 2
			elif pair_value_list[0] in medium_values_list and pair_value_list[1] in medium_values_list:
				actual_choice_index = 3
			elif (pair_value_list[0] in medium_values_list and pair_value_list[1] in low_values_list) or (pair_value_list[0] in low_values_list and pair_value_list[1] in medium_values_list):
				actual_choice_index = 4
			elif pair_value_list[0] in low_values_list and pair_value_list[1] in low_values_list:
				actual_choice_index = 5
			player['Decision'] = l_matrices['decision_before_turn_highest_bet_two_pair'][player_type_index][actual_choice_index]
		elif len(pair_value_list) == 1:
			player['Function'] = 'Bet224'
			if pair_value_list[0] in high_values_list:
				actual_choice_index = 0
			elif pair_value_list[0] in medium_values_list:
				actual_choice_index = 1
			elif pair_value_list[0] in low_values_list:
				actual_choice_index = 2
			player['Decision'] = l_matrices['decision_before_turn_highest_bet_one_pair'][player_type_index][actual_choice_index]
	
#decision_before_turn_highest_bet_in_range_of_royal_flush AND decision_before_turn_highest_bet_in_range_of_straight_flush AND decision_before_turn_highest_bet_in_range_of_royal_flush_and_straight_flush
def bet225_and_bet226_and_bet227(player,player_type_index,card_count):
	global community_cards
	global l_matrices
	global l_value_order1
	global l_suite_order
	actual_choice_index = -1
	local_card_list = []
	card_suite_list = [0,0,0,0]
	suite_to_be_checked = ''
	cards_to_check_list = []
	count_cards = 1
	values_list = []
	checkable_suites = []
	low_value = ''
	count = 0
	count1 = 0
	ace_there = False
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	for card in local_card_list:
		card_suite_list[l_suite_order.index(card['Suite'])] += 1
	for num in card_suite_list:
		if num >= 3:
			checkable_suites.append(l_suite_order[count])
			break
		count += 1
	count = 0
	if checkable_suites != []:
		for suite_to_be_checked in checkable_suites:
			for card in local_card_list:
				if card['Suite'] == suite_to_be_checked:
					cards_to_check_list.append(card)
					values_list.append(card['Value'])
			for value in values_list:
				if value == '10' or value == 'J' or value == 'Q' or value == 'K' or value == 'A':
					count += 1
			for value in values_list:
				if value == 'A' and count >= 3:
					ace_there = True
					player['Function'] = 'Bet225'
					actual_choice_index = count - 3
					player['Decision'] = l_matrices['decision_before_turn_highest_bet_in_range_of_royal_flush'][player_type_index][actual_choice_index]
					break

			low_value = 'K'
			for value in values_list:
				if player['Decision'] != '':
					break
				else:
					low_value = value
					for value in values_list:
						if l_value_order1.index(value) in range(l_value_order1.index(low_value), l_value_order1.index(low_value) + 5):
							count1 += 1
					if count1 >= 3 and count < 3:
						player['Function'] = 'Bet226'
						actual_choice_index = l_suite_order.index(cards_to_check_list[0]['Suite'])
						player['Decision'] = l_matrices['decision_before_turn_highest_bet_in_range_of_straight_flush'][player_type_index][actual_choice_index]
					elif (not ace_there) and (count >= 3):
						player['Function'] = 'Bet227'
						actual_choice_index = count - 3
						player['Decision'] = l_matrices['decision_before_turn_highest_bet_in_range_of_royal_flush_and_straight_flush'][player_type_index][actual_choice_index]

#decision_before_turn_highest_bet_in_range_of_flush
def bet228(player,player_type_index,card_count):
	global l_matrices
	global l_suite_order
	global community_cards
	card_suite_list = [0,0,0,0]
	local_card_list = []
	count_cards = 1
	actual_choice_index = -1
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append(community_cards[count_cards - 3]['Suite'])
		else:
			if count_cards == 1:
				local_card_list.append(player['Card1_Suite'])
			else:
				local_card_list.append(player['Card2_Suite'])
		count_cards += 1
	for suite in local_card_list:
		card_suite_list[l_suite_order.index(suite)] += 1
	for num in card_suite_list:
		if num >= 3:
			player['Function'] = 'Bet228'
			actual_choice_index = card_suite_list.index(num)
			player['Decision'] = l_matrices['decision_before_turn_highest_bet_in_range_of_flush'][player_type_index][actual_choice_index]
			break

#decision_before_turn_highest_bet_in_range_of_straight
def bet229(player,player_type_index,card_count):
	global l_matrices
	global community_cards
	global l_value_order
	global l_value_order1
	local_card_list = []
	count_cards = 1
	actual_choice_index = -1
	lowest_card = {}
	count = 0
	in_range_cards_count = 0
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Suite' : community_cards[count_cards - 3]['Suite'], 'Value' : community_cards[count_cards - 3]['Value']})
		else:
			if count_cards == 1:
				local_card_list.append({'Suite' : player['Card1_Suite'], 'Value' : player['Card1_Value']})
			else:
				local_card_list.append({'Suite' : player['Card2_Suite'], 'Value' : player['Card2_Value']})
		count_cards += 1
	lowest_card = local_card_list[0]
	for card in local_card_list:
		count = 0
		lowest_card = card
		for card1 in local_card_list:
			if l_value_order.index(card1['Value']) in range(l_value_order.index(lowest_card['Value']),l_value_order.index(lowest_card['Value']) + 5):
				count += 1
		if (count >= 3) and (count > in_range_cards_count):
			player['Function'] = 'Bet229'
			actual_choice_index = count - 3
			player['Decision'] = l_matrices['decision_before_turn_highest_bet_in_range_of_straight'][player_type_index][actual_choice_index]

	if player['Decision'] == '':
		count = 0
		in_range_cards_count = 0
		for card in local_card_list:
			count = 0
			lowest_card = card
			for card1 in local_card_list:
				if l_value_order1.index(card1['Value']) in range(l_value_order1.index(lowest_card['Value']),l_value_order1.index(lowest_card['Value']) + 5):
					count += 1
			if (count >= 3) and (count > in_range_cards_count):
				player['Function'] = 'Bet229'
				actual_choice_index = count - 3
				player['Decision'] = l_matrices['decision_before_turn_highest_bet_in_range_of_straight'][player_type_index][actual_choice_index]

#decision_before_turn_highest_bet_all_distinct_cards
def bet230(player,player_type_index,card_count):
	global l_matrices
	global low_values_list
	global medium_values_list
	global high_values_list
	global l_value_order
	global l_suite_order
	local_card_list = []
	actual_choice_index = -1
	count_cards = 1
	highest_card = {}
	for num in range(1,card_count + 1):
		if count_cards >= 3:
			local_card_list.append({'Value' : community_cards[count_cards - 3]['Value'], 'Suite' : community_cards[count_cards - 3]['Suite']})
		else:
			if count_cards == 1:
				local_card_list.append({'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite']})
			else:
				local_card_list.append({'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite']})
		count_cards += 1
	highest_card = local_card_list[0]
	for card in local_card_list:
		if l_value_order.index(card['Value']) > l_value_order.index(highest_card['Value']):
			highest_card = card
	player['Function'] = 'Bet230'
	actual_choice_index = l_suite_order.index(highest_card['Suite'])
	if highest_card['Value'] in high_values_list:
		actual_choice_index *= 3
	elif highest_card['Value'] in medium_values_list:
		actual_choice_index = (actual_choice_index * 3) + 1
	elif highest_card['Value'] in low_values_list1:
		actual_choice_index = (actual_choice_index * 3) + 2
	player['Decision'] = l_matrices['decision_before_turn_highest_bet_all_distinct_cards'][player_type_index][actual_choice_index]

#second round of betting (flop)
def bet2(first_hand_yes):
	global betting_temp_player_list
	global high_values_list
	global medium_values_list
	global low_values_list
	global raise_amount
	global big_blind_amount
	global small_blind_amount
	global big_blind
	global small_blind
	matrix_name = ''
	player_type_index = 0
	last_player_to_raise = ''
	all_in = False
	amount_to_match = 0
	previous_raise_amount = 0
	player_who_put_all_in = ''
	return_list = []
	extra_money = []
	extra_money_value = 0
	skip_betting = False
	one_player_left = False
	count = 0
	first_hand_yes = first_hand_yes
	index_count = 0
	winner_counter = 0
	active_player_count = 0

	for player in betting_temp_player_list:
		extra_money.append(0)

	for player in betting_temp_player_list:
		if player['Folded?'] != True:
			amount_to_match = player['Money']
	
	for player1 in betting_temp_player_list:
		if player1['Decision'] == 'Fold':
			count += 1

	if count == len(betting_temp_player_list) - 1:
		one_player_left = True

	for player in betting_temp_player_list:
		if one_player_left == True:
			break
		else:
			active_player_count = 0
			if player['Folded?'] == False:
				player_type_index = determine_player_type_indexes(player)
				if player['Player_Type'] != 'Human':
					QLearningState = Q_Learning(player['Name'], 2, True, last_player_to_raise, amount_to_match, betting_temp_player_list.index(player), False)
					QLearningState.training()

					player['Decision'] = max(q_tables[0][player['Name']], key=q_tables[0][player['Name']].get)
				return_list = bet(player,amount_to_match,last_player_to_raise,False,False,False,first_hand_yes,2)
				amount_to_match = return_list[0]
				last_player_to_raise = return_list[1]

				if return_list[2] > 0:
					extra_money[index_count] = (return_list[2])

				for player in betting_temp_player_list:
					if player['Folded?'] != True:
						active_player_count += 1

				if active_player_count == 1:
					one_player_left = True
				
		index_count += 1

	#run through player second time until last player to raise
	index_count = 0
	for player in betting_temp_player_list:
		if one_player_left == True:
			break
		else:
			if player['Folded?'] == False:
				if last_player_to_raise == '':
					break
				else:
					player_type_index = determine_player_type_indexes(player)
					active_player_count = 0
					if player['Name'] == last_player_to_raise:
						break
					else:
						if player['Player_Type'] != 'Human':
							QLearningState = Q_Learning(player['Name'], 2, False, last_player_to_raise, amount_to_match, betting_temp_player_list.index(player), False)
							QLearningState.training()

							player['Decision'] = max(q_tables[0][player['Name']], key=q_tables[0][player['Name']].get)

					return_list = bet(player,amount_to_match,last_player_to_raise,True,True,False,first_hand_yes,2)
					amount_to_match = return_list[0]
					last_player_to_raise = return_list[1]

					if return_list[2] > 0:
						extra_money[index_count] = return_list[2]

					for player in betting_temp_player_list:
						if player['Folded?'] != True:
							active_player_count += 1

					if active_player_count == 1:
						one_player_left = True
					
		index_count += 1
	
	skip_betting = redistribute_money(extra_money,skip_betting,last_player_to_raise)
	return [skip_betting,one_player_left]

#third round of betting (turn)
def bet3(first_hand_yes):
	global betting_temp_player_list
	global high_values_list
	global medium_values_list
	global low_values_list
	global raise_amount
	global big_blind_amount
	global small_blind_amount
	global big_blind
	global small_blind
	matrix_name = ''
	player_type_index = 0
	last_player_to_raise = ''
	all_in = False
	amount_to_match = 0
	previous_raise_amount = 0
	player_who_put_all_in = ''
	return_list = []
	extra_money = []
	extra_money_value = 0
	skip_betting = False
	one_player_left = False
	count = 0
	first_hand_yes = first_hand_yes
	index_count = 0
	winner_counter = 0
	active_player_count = 0

	for player in betting_temp_player_list:
		extra_money.append(0)

	for player in betting_temp_player_list:
		if player['Folded?'] != True:
			amount_to_match = player['Money']
	
	for player1 in betting_temp_player_list:
		if player1['Decision'] == 'Fold':
			count += 1

	if count == len(betting_temp_player_list) - 1:
		one_player_left = True

	for player in betting_temp_player_list:
		if one_player_left == True:
			break
		else:
			active_player_count = 0
			if player['Folded?'] == False:
				player_type_index = determine_player_type_indexes(player)
				if player['Player_Type'] != 'Human':
					QLearningState = Q_Learning(player['Name'], 3, True, last_player_to_raise, amount_to_match, betting_temp_player_list.index(player), False)
					QLearningState.training()

					player['Decision'] = max(q_tables[0][player['Name']], key=q_tables[0][player['Name']].get)
					
				return_list = bet(player,amount_to_match,last_player_to_raise,False,False,False,first_hand_yes,3)
				amount_to_match = return_list[0]
				last_player_to_raise = return_list[1]

				if return_list[2] > 0:
					extra_money[index_count] = (return_list[2])

				for player in betting_temp_player_list:
					if player['Folded?'] != True:
						active_player_count += 1

				if active_player_count == 1:
					one_player_left = True
				
		index_count += 1

	#run through player second time until last player to raise
	index_count = 0
	for player in betting_temp_player_list:
		if one_player_left == True:
			break
		else:
			if player['Folded?'] == False:
				if last_player_to_raise == '':
					break
				else:
					player_type_index = determine_player_type_indexes(player)
					active_player_count = 0
					if player['Name'] == last_player_to_raise:
						break
					else:
						if player['Player_Type'] != 'Human':
							QLearningState = Q_Learning(player['Name'], 3, False, last_player_to_raise, amount_to_match, betting_temp_player_list.index(player), False)
							QLearningState.training()

							player['Decision'] = max(q_tables[0][player['Name']], key=q_tables[0][player['Name']].get)
					return_list = bet(player,amount_to_match,last_player_to_raise,True,True,False,first_hand_yes,3)
					amount_to_match = return_list[0]
					last_player_to_raise = return_list[1]

					if return_list[2] > 0:
						extra_money[index_count] = return_list[2]

					for player in betting_temp_player_list:
						if player['Folded?'] != True:
							active_player_count += 1

					if active_player_count == 1:
						one_player_left = True
					
		index_count += 1
	
	skip_betting = redistribute_money(extra_money,skip_betting,last_player_to_raise)

	return [skip_betting,one_player_left]

#fourth round of betting (river)
def bet4(first_hand_yes):
	global betting_temp_player_list
	global high_values_list
	global medium_values_list
	global low_values_list
	global raise_amount
	global big_blind_amount
	global small_blind_amount
	global big_blind
	global small_blind
	matrix_name = ''
	player_type_index = 0
	last_player_to_raise = ''
	all_in = False
	amount_to_match = 0
	previous_raise_amount = 0
	player_who_put_all_in = ''
	return_list = []
	extra_money = []
	extra_money_value = 0
	skip_betting = False
	one_player_left = False
	count = 0
	first_hand_yes = first_hand_yes
	index_count = 0
	winner_counter = 0
	active_player_count = 0

	for player in betting_temp_player_list:
		extra_money.append(0)

	for player in betting_temp_player_list:
		if player['Folded?'] != True:
			amount_to_match = player['Money']
	
	for player1 in betting_temp_player_list:
		if player1['Decision'] == 'Fold':
			count += 1

	if count == len(betting_temp_player_list) - 1:
		one_player_left = True

	for player in betting_temp_player_list:
		if one_player_left == True:
			break
		else:
			active_player_count = 0
			if player['Folded?'] == False:
				player_type_index = determine_player_type_indexes(player)
				if player['Player_Type'] != 'Human':
					QLearningState = Q_Learning(player['Name'], 4, True, last_player_to_raise, amount_to_match, betting_temp_player_list.index(player), False)
					QLearningState.training()

					player['Decision'] = max(q_tables[0][player['Name']], key=q_tables[0][player['Name']].get)
				return_list = bet(player,amount_to_match,last_player_to_raise,False,False,False,first_hand_yes,4)
				amount_to_match = return_list[0]
				last_player_to_raise = return_list[1]

				if return_list[2] > 0:
					extra_money[index_count] = (return_list[2])

				for player in betting_temp_player_list:
					if player['Folded?'] != True:
						active_player_count += 1

				if active_player_count == 1:
					one_player_left = True

		index_count += 1

	#run through player second time until last player to raise
	index_count = 0
	for player in betting_temp_player_list:
		if one_player_left == True:
			break
		else:
			if player['Folded?'] == False:
				if last_player_to_raise == '':
					break
				else:
					player_type_index = determine_player_type_indexes(player)
					active_player_count = 0
					if player['Name'] == last_player_to_raise:
						break
					else:
						if player['Player_Type'] != 'Human':
							QLearningState = Q_Learning(player['Name'], 4, False, last_player_to_raise, amount_to_match, betting_temp_player_list.index(player), False)
							QLearningState.training()

							player['Decision'] = max(q_tables[0][player['Name']], key=q_tables[0][player['Name']].get)
					return_list = bet(player,amount_to_match,last_player_to_raise,True,True,False,first_hand_yes,4)
					amount_to_match = return_list[0]
					last_player_to_raise = return_list[1]

					if return_list[2] > 0:
						extra_money[index_count] = return_list[2]

					for player in betting_temp_player_list:
						if player['Folded?'] != True:
							active_player_count += 1

					if active_player_count == 1:
						one_player_left = True

		index_count += 1
	
	skip_betting = redistribute_money(extra_money,skip_betting,last_player_to_raise)

	return [skip_betting,one_player_left]

#return highest card in a set of cards
def get_high_card_of_combo(l_cards):
	global l_value_order
	global l_suite_order
	high_card = l_cards[0]
	for card in l_cards:
		if (card['Value'] == high_card['Value']):
			if l_suite_order.index(card['Suite']) > l_suite_order.index(high_card['Suite']):
				high_card = card
		else:
			if l_value_order.index(card['Value']) > l_value_order.index(high_card['Value']):
				high_card = card
	return high_card

#checks if a player has a royal flush
def is_royal_flush(player):
	global community_cards
	global correct_combo
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	correct_combo = []
	five_card_combos = [[c1,c2,c3,c4,c5], [c1,c2,c3,c4,c6], [c1,c2,c3,c4,c7],
						[c1,c2,c3,c5,c6], [c1,c2,c3,c5,c7],
						[c1,c2,c3,c6,c7],
						[c1,c2,c4,c5,c6], [c1,c2,c4,c5,c7],
						[c1,c2,c4,c6,c7],
						[c1,c2,c5,c6,c7],
						[c1,c3,c4,c5,c6], [c1,c3,c4,c5,c7],
						[c1,c3,c4,c6,c7],
						[c1,c3,c5,c6,c7],
						[c1,c4,c5,c6,c7],
						[c2,c3,c4,c5,c6], [c2,c3,c4,c5,c7],
						[c2,c3,c4,c6,c7],
						[c2,c3,c5,c6,c7],
						[c2,c4,c5,c6,c7],
						[c3,c4,c5,c6,c7]]
	num_combos = [[1,13,12,11,10], [14,26,25,24,23], [27,39,38,37,36], [40,52,51,50,49]]
	count = 0
	element_count = 0
	combo_count = 0
	for element in five_card_combos:
		for combo in num_combos:
			for card in element:
				for num in range(0,5):
					if (card['Number'] == combo[num]):
						count += 1
			if (count >= 5):
				correct_combo.append(element)
			count = 0
	return correct_combo

#checks if a player has a straight flush
def is_straight_flush(player):
	global community_cards
	global correct_combo
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	correct_combo = []
	five_card_combos = [[c1,c2,c3,c4,c5], [c1,c2,c3,c4,c6], [c1,c2,c3,c4,c7],
						[c1,c2,c3,c5,c6], [c1,c2,c3,c5,c7],
						[c1,c2,c3,c6,c7],
						[c1,c2,c4,c5,c6], [c1,c2,c4,c5,c7],
						[c1,c2,c4,c6,c7],
						[c1,c2,c5,c6,c7],
						[c1,c3,c4,c5,c6], [c1,c3,c4,c5,c7],
						[c1,c3,c4,c6,c7],
						[c1,c3,c5,c6,c7],
						[c1,c4,c5,c6,c7],
						[c2,c3,c4,c5,c6], [c2,c3,c4,c5,c7],
						[c2,c3,c4,c6,c7],
						[c2,c3,c5,c6,c7],
						[c2,c4,c5,c6,c7],
						[c3,c4,c5,c6,c7]]
	straight_flush = False
	same_suite = False
	for element in five_card_combos:
		straight_flush = False
		same_suite = are_same_suite(element)
		if (same_suite == True):
			smallest_value = smallest(element)
			straight_flush = True
			for elem in element:
				if not (elem['Number'] in range(smallest_value, smallest_value + 5)):
					straight_flush = False
					break
		if (straight_flush == True):
			correct_combo.append(element)
	
	
	#return highest possible straight flush
	l_high_cards = []
	for elem in correct_combo:
		l_high_cards.append(get_high_card_of_combo(elem))
	return_combo = []
	if l_high_cards != []:
		highest_card = get_high_card_of_combo(l_high_cards)
		for elem in correct_combo:
			if highest_card in elem:
				return_combo.append(elem)
	
	return return_combo

#checks if a player has a four of a kind
def is_four_of_a_kind(player):
	global community_cards
	global correct_combo
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	combined_card_list = [c1,c2,c3,c4,c5,c6,c7]
	correct_combo = []
	remaining_cards = []
	four_card_combos = [[c1,c2,c3,c4], [c1,c2,c3,c5], [c1,c2,c3,c6], [c1,c2,c3,c7],
						[c1,c2,c4,c5], [c1,c2,c4,c6], [c1,c2,c4,c7],
						[c1,c2,c5,c6], [c1,c2,c5,c7],
						[c1,c2,c6,c7],
						[c1,c3,c4,c5], [c1,c3,c4,c6], [c1,c3,c4,c7],
						[c1,c3,c5,c6], [c1,c3,c5,c7],
						[c1,c3,c6,c7],
						[c1,c4,c5,c6], [c1,c4,c5,c7],
						[c1,c4,c6,c7],
						[c1,c5,c6,c7],
						[c2,c3,c4,c5], [c2,c3,c4,c6], [c2,c3,c4,c7],
						[c2,c3,c5,c6], [c2,c3,c5,c7],
						[c2,c3,c6,c7],
						[c2,c4,c5,c6], [c2,c4,c5,c7],
						[c2,c4,c6,c7],
						[c2,c5,c6,c7],
						[c3,c4,c5,c6], [c3,c4,c5,c7],
						[c3,c4,c6,c7],
						[c3,c5,c6,c7],
						[c4,c5,c6,c7]]
	for element in four_card_combos:
		if (element[0]['Value'] == element[1]['Value'] == element[2]['Value'] == element[3]['Value']):
			correct_combo.append(element)
	
	if len(correct_combo) > 0:
		for card in combined_card_list:
			if card not in correct_combo[0]:
				remaining_cards.append(card)

		correct_combo[0].append(get_high_card_of_combo(remaining_cards))

	return correct_combo

#checks if a player has a full house
def is_full_house(player):
	global community_cards
	global correct_combo
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number'], 'Weight' : player['Card1_Weight']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number'], 'Weight' : player['Card2_Weight']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	correct_combo = []
	five_card_combos = [[c1,c2,c3,c4,c5], [c1,c2,c3,c4,c6], [c1,c2,c3,c4,c7],
						[c1,c2,c3,c5,c6], [c1,c2,c3,c5,c7],
						[c1,c2,c3,c6,c7],
						[c1,c2,c4,c5,c6], [c1,c2,c4,c5,c7],
						[c1,c2,c4,c6,c7],
						[c1,c2,c5,c6,c7],
						[c1,c3,c4,c5,c6], [c1,c3,c4,c5,c7],
						[c1,c3,c4,c6,c7],
						[c1,c3,c5,c6,c7],
						[c1,c4,c5,c6,c7],
						[c2,c3,c4,c5,c6], [c2,c3,c4,c5,c7],
						[c2,c3,c4,c6,c7],
						[c2,c3,c5,c6,c7],
						[c2,c4,c5,c6,c7],
						[c3,c4,c5,c6,c7]]
	full_house_card_combos = [[0,1,2,3,4],[0,1,3,2,4],[0,1,4,2,3],
							  [0,2,3,1,4],[0,2,4,1,3],
							  [0,3,4,1,2],
							  [1,2,3,0,4],[1,2,4,0,3],
							  [1,3,4,0,2],
							  [2,3,4,0,1]]
	for element in five_card_combos:
		for num_combo in full_house_card_combos:
			if element[num_combo[0]]['Value'] == element[num_combo[1]]['Value'] == element[num_combo[2]]['Value']:
				if ((element[num_combo[3]]['Value'] == element[num_combo[4]]['Value']) and
					(element[num_combo[3]]['Value'] != element[num_combo[0]]['Value'])):
					correct_combo.append(element)

	for i in range(0,len(correct_combo) - 1):
		for j in range (i+1, len(correct_combo)):
			if sum_of_weights(correct_combo[i]) < sum_of_weights(correct_combo[j]):
				temp_list = correct_combo[i].copy()
				correct_combo[i] = correct_combo[j].copy()
				correct_combo[j] = temp_list.copy()

	return correct_combo

#checks if a player has a flush
def is_flush(player):
	global community_cards
	global correct_combo
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	correct_combo = []
	five_card_combos = [[c1,c2,c3,c4,c5], [c1,c2,c3,c4,c6], [c1,c2,c3,c4,c7],
						[c1,c2,c3,c5,c6], [c1,c2,c3,c5,c7],
						[c1,c2,c3,c6,c7],
						[c1,c2,c4,c5,c6], [c1,c2,c4,c5,c7],
						[c1,c2,c4,c6,c7],
						[c1,c2,c5,c6,c7],
						[c1,c3,c4,c5,c6], [c1,c3,c4,c5,c7],
						[c1,c3,c4,c6,c7],
						[c1,c3,c5,c6,c7],
						[c1,c4,c5,c6,c7],
						[c2,c3,c4,c5,c6], [c2,c3,c4,c5,c7],
						[c2,c3,c4,c6,c7],
						[c2,c3,c5,c6,c7],
						[c2,c4,c5,c6,c7],
						[c3,c4,c5,c6,c7]]
	for element in five_card_combos:
		same_suite = are_same_suite(element)
		if same_suite == True:
			correct_combo.append(element)
	l_high_cards = []
	for elem in correct_combo:
		l_high_cards.append(get_high_card_of_combo(elem))
	return_combo = []
	if l_high_cards != []:
		highest_card = get_high_card_of_combo(l_high_cards)
		for elem in correct_combo:
			if highest_card in elem:
				return_combo.append(elem)
	return return_combo

#checks if a player has a straight (ace-high)
def is_straight(player):
	global community_cards
	global correct_combo
	global l_value_order
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number'], 'Weight' : player['Card1_Weight']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number'], 'Weight' : player['Card2_Weight']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	correct_combo = []
	five_card_combos = [[c1,c2,c3,c4,c5], [c1,c2,c3,c4,c6], [c1,c2,c3,c4,c7],
						[c1,c2,c3,c5,c6], [c1,c2,c3,c5,c7],
						[c1,c2,c3,c6,c7],
						[c1,c2,c4,c5,c6], [c1,c2,c4,c5,c7],
						[c1,c2,c4,c6,c7],
						[c1,c2,c5,c6,c7],
						[c1,c3,c4,c5,c6], [c1,c3,c4,c5,c7],
						[c1,c3,c4,c6,c7],
						[c1,c3,c5,c6,c7],
						[c1,c4,c5,c6,c7],
						[c2,c3,c4,c5,c6], [c2,c3,c4,c5,c7],
						[c2,c3,c4,c6,c7],
						[c2,c3,c5,c6,c7],
						[c2,c4,c5,c6,c7],
						[c3,c4,c5,c6,c7]]
	value_list = []
	flag_straight = True
	for element in five_card_combos:
		value_list = []
		flag_straight = True
		small_val = smallest_value_order(element)
		if not (are_same_suite(element)):
			for elem in element:
				if not (l_value_order.index(elem['Value']) in range(l_value_order.index(small_val), l_value_order.index(small_val) + 5)):
					flag_straight = False
					break
				else:
					if elem['Value'] not in value_list:
						value_list.append(elem['Value'])
			if (flag_straight == True and len(value_list) == 5):
				correct_combo.append(element)

	for i in range(0,len(correct_combo) - 1):
		for j in range (i+1, len(correct_combo)):
			if sum_of_weights(correct_combo[i]) < sum_of_weights(correct_combo[j]):
				temp_list = correct_combo[i].copy()
				correct_combo[i] = correct_combo[j].copy()
				correct_combo[j] = temp_list.copy()
	return correct_combo

#checks if a player has a straight (king-high)
def is_straight1(player):
	global community_cards
	global correct_combo
	global l_value_order1
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number'], 'Weight' : player['Card1_Weight']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number'], 'Weight' : player['Card2_Weight']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	correct_combo = []
	five_card_combos = [[c1,c2,c3,c4,c5], [c1,c2,c3,c4,c6], [c1,c2,c3,c4,c7],
						[c1,c2,c3,c5,c6], [c1,c2,c3,c5,c7],
						[c1,c2,c3,c6,c7],
						[c1,c2,c4,c5,c6], [c1,c2,c4,c5,c7],
						[c1,c2,c4,c6,c7],
						[c1,c2,c5,c6,c7],
						[c1,c3,c4,c5,c6], [c1,c3,c4,c5,c7],
						[c1,c3,c4,c6,c7],
						[c1,c3,c5,c6,c7],
						[c1,c4,c5,c6,c7],
						[c2,c3,c4,c5,c6], [c2,c3,c4,c5,c7],
						[c2,c3,c4,c6,c7],
						[c2,c3,c5,c6,c7],
						[c2,c4,c5,c6,c7],
						[c3,c4,c5,c6,c7]]
	value_list = []
	flag_straight = True
	for element in five_card_combos:
		value_list = []
		flag_straight = True
		small_val1 = smallest_value_order1(element)
		if not (are_same_suite(element)):
			for elem in element:
				if not (l_value_order1.index(elem['Value']) in range(l_value_order1.index(small_val1), l_value_order1.index(small_val1) + 5)):
					flag_straight = False
					break
				else:
					if elem['Value'] not in value_list:
						value_list.append(elem['Value'])
			if (flag_straight == True and len(value_list) == 5):
				correct_combo.append(element)

	for i in range(0,len(correct_combo) - 1):
		for j in range (i+1, len(correct_combo)):
			if sum_of_weights(correct_combo[i]) < sum_of_weights(correct_combo[j]):
				temp_list = correct_combo[i].copy()
				correct_combo[i] = correct_combo[j].copy()
				correct_combo[j] = temp_list.copy()
	return correct_combo

#checks if a player has a three of a kind
def is_three_of_a_kind(player):
	global community_cards
	global correct_combo
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	combined_card_list = [c1,c2,c3,c4,c5,c6,c7]
	remaining_cards = []
	correct_combo = []
	three_card_combos = [[c1,c2,c3], [c1,c2,c4], [c1,c2,c5], [c1,c2,c6], [c1,c2,c7],
						 [c1,c3,c4], [c1,c3,c5], [c1,c3,c6], [c1,c3,c7],
						 [c1,c4,c5], [c1,c4,c6], [c1,c4,c7],
						 [c1,c5,c6], [c1,c5,c7],
						 [c1,c6,c7],
						 [c2,c3,c4], [c2,c3,c5], [c2,c3,c6], [c2,c3,c7],
						 [c2,c4,c5], [c2,c4,c6], [c2,c4,c7],
						 [c2,c5,c6], [c2,c5,c7],
						 [c2,c6,c7],
						 [c3,c4,c5], [c3,c4,c6], [c3,c4,c7],
						 [c3,c5,c6], [c3,c5,c7],
						 [c3,c6,c7],
						 [c4,c5,c6], [c4,c5,c7],
						 [c4,c6,c7],
						 [c5,c6,c7]]
	count = 0
	for element in three_card_combos:
		if (element[0]['Value'] == element[1]['Value'] == element[2]['Value']):
			count += 1
			correct_combo.append(element)

	if (len(correct_combo) == 1):
		for card in combined_card_list:
			if card not in correct_combo[0]:
				remaining_cards.append(card)

		correct_combo[0].append(get_high_card_of_combo(remaining_cards))
		remaining_cards.remove(get_high_card_of_combo(remaining_cards))
		correct_combo[0].append(get_high_card_of_combo(remaining_cards))

	return correct_combo if count == 1 else []

#checks if a player has two pair
def is_two_pair(player):
	global community_cards
	global correct_combo
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number'], 'Weight' : player['Card1_Weight']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number'], 'Weight' : player['Card2_Weight']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	combined_card_list = [c1,c2,c3,c4,c5,c6,c7]
	remaining_cards = []
	two_card_combos = [[c1, c2], [c1, c3], [c1, c4], [c1, c5], [c1, c6], [c1, c7],
					   [c2, c3], [c2, c4], [c2, c5], [c2, c6], [c2, c7],
					   [c3, c4], [c3, c5], [c3, c6], [c3, c7],
					   [c4, c5], [c4, c6], [c4, c7],
					   [c5, c6], [c5, c7],
					   [c6, c7]]
	count = 0
	value_list = []
	correct_combo = []
	for element in two_card_combos:
		if ((element[0]['Value'] == element[1]['Value']) and (element[0]['Value'] not in value_list)):
			count += 1
			correct_combo.append(element)
			value_list.append(element)
	return_combo = []
	if count == 2:
		if (l_value_order.index(correct_combo[0][0]['Value']) > l_value_order.index(correct_combo[1][0]['Value'])):
			return_combo.append(correct_combo[0][0])
			return_combo.append(correct_combo[0][1])
			return_combo.append(correct_combo[1][1])
			return_combo.append(correct_combo[1][1])
		else:
			return_combo.append(correct_combo[1][0])
			return_combo.append(correct_combo[1][1])
			return_combo.append(correct_combo[0][1])
			return_combo.append(correct_combo[0][1])
		for card in combined_card_list:
			if card not in return_combo:
				remaining_cards.append(card)
		return_combo.append(get_high_card_of_combo(remaining_cards))
	elif count == 3:
		if (l_value_order.index(correct_combo[0][0]['Value']) > l_value_order.index(correct_combo[1][0]['Value'])) and (l_value_order.index(correct_combo[0][0]['Value']) > l_value_order.index(correct_combo[2][0]['Value'])):
			return_combo.append(correct_combo[0][0])
			return_combo.append(correct_combo[0][1])
			if (l_value_order.index(correct_combo[1][0]['Value']) > l_value_order.index(correct_combo[2][0]['Value'])):
				return_combo.append(correct_combo[1][0])
				return_combo.append(correct_combo[1][1])
			else:
				return_combo.append(correct_combo[2][0])
				return_combo.append(correct_combo[2][1])
		elif (l_value_order.index(correct_combo[1][0]['Value']) > l_value_order.index(correct_combo[0][0]['Value'])) and (l_value_order.index(correct_combo[1][0]['Value']) > l_value_order.index(correct_combo[2][0]['Value'])):
			return_combo.append(correct_combo[1][0])
			return_combo.append(correct_combo[1][1])
			if (l_value_order.index(correct_combo[0][0]['Value']) > l_value_order.index(correct_combo[2][0]['Value'])):
				return_combo.append(correct_combo[0][0])
				return_combo.append(correct_combo[0][1])
			else:
				return_combo.append(correct_combo[2][0])
				return_combo.append(correct_combo[2][1])
		elif (l_value_order.index(correct_combo[2][0]['Value']) > l_value_order.index(correct_combo[0][0]['Value'])) and (l_value_order.index(correct_combo[2][0]['Value']) > l_value_order.index(correct_combo[1][0]['Value'])):
			return_combo.append(correct_combo[2][0])
			return_combo.append(correct_combo[2][1])
			if (l_value_order.index(correct_combo[0][0]['Value']) > l_value_order.index(correct_combo[1][0]['Value'])):
				return_combo.append(correct_combo[0][0])
				return_combo.append(correct_combo[0][1])
			else:
				return_combo.append(correct_combo[1][0])
				return_combo.append(correct_combo[1][1])

		for card in combined_card_list:
			if card not in return_combo:
				remaining_cards.append(card)
		return_combo.append(get_high_card_of_combo(remaining_cards))

	return return_combo

#checks if a player has one pair
def is_one_pair(player):
	global community_cards
	global correct_combo
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	two_card_combos = [[c1, c2], [c1, c3], [c1, c4], [c1, c5], [c1, c6], [c1, c7],
					   [c2, c3], [c2, c4], [c2, c5], [c2, c6], [c2, c7],
					   [c3, c4], [c3, c5], [c3, c6], [c3, c7],
					   [c4, c5], [c4, c6], [c4, c7],
					   [c5, c6], [c5, c7],
					   [c6, c7]]
	count = 0
	correct_combo = []
	combined_card_list = [c1,c2,c3,c4,c5,c6,c7]
	remaining_cards = []
	for element in two_card_combos:
		if (element[0]['Value'] == element[1]['Value']):
			count += 1 
			correct_combo.append(element)

	if len(correct_combo) == 1:
		for card in combined_card_list:
			if card not in correct_combo[0]:
				remaining_cards.append(card)

		correct_combo[0].append(get_high_card_of_combo(remaining_cards))
		remaining_cards.remove(get_high_card_of_combo(remaining_cards))
		correct_combo[0].append(get_high_card_of_combo(remaining_cards))
		remaining_cards.remove(get_high_card_of_combo(remaining_cards))
		correct_combo[0].append(get_high_card_of_combo(remaining_cards))

	return correct_combo

#returns the high card of a player's hand
def get_high_card(player):
	global l_value_order
	global l_suite_order
	c1 = {'Value' : player['Card1_Value'], 'Suite' : player['Card1_Suite'], 'Number' : player['Card1_Number'], 'Weight' : player['Card1_Weight']}
	c2 = {'Value' : player['Card2_Value'], 'Suite' : player['Card2_Suite'], 'Number' : player['Card2_Number'], 'Weight' : player['Card2_Weight']}
	c3 = community_cards[0]
	c4 = community_cards[1]
	c5 = community_cards[2]
	c6 = community_cards[3]
	c7 = community_cards[4]
	combined_card_list = [c1,c2,c3,c4,c5,c6,c7]
	correct_combo = [[]]
	
	for i in range(0,5):
		correct_combo[0].append(get_high_card_of_combo(combined_card_list))
		combined_card_list.remove(get_high_card_of_combo(combined_card_list))

	return correct_combo

#returns whether the given cards are the same suite
def are_same_suite(l_nos):
	if (l_nos[0]['Suite'] == l_nos[1]['Suite'] == l_nos[2]['Suite'] == l_nos[3]['Suite'] == l_nos[4]['Suite']):
		return True
	else:
		return False

#returns the smallest card of the given cards
def smallest(l_nos):
	small_val = l_nos[0]['Number']
	for elem in l_nos:
		if elem['Number'] <= small_val:
			small_val = elem['Number']
	return small_val

#returns the sum of the weights of all the cards given
def sum_of_weights(l_list):
	my_sum = 0
	for e in l_list:
		my_sum = my_sum + e['Weight']
	return my_sum

#returns the cards in a full house sorted into three and two
def full_house_sort(l_five_cards):
	global l_value_order

	count = 0
	one_value = l_five_cards[0]['Value']
	for i in range(1, len(l_five_cards)):
		if l_five_cards[i]['Value'] == one_value:
			count += 1

	ordered = []
	if count == 2:
		for card in l_five_cards:
			if card['Value'] == one_value:
				ordered.append(card)
			if len(ordered) == 3:
				break
		for card in l_five_cards:
			if card['Value'] != one_value:
				ordered.append(card)
			if len(ordered) == 5:
				break
	else:
		for card in l_five_cards:
			if card['Value'] != one_value:
				ordered.append(card)
			if len(ordered) == 3:
				break
		for card in l_five_cards:
			if card['Value'] == one_value:
				ordered.append(card)
			if len(ordered) == 5:
				break

	return ordered

#sorts the given cards into highest to lowest order
def sort_cards(l_five_cards):
	for index1 in range(0,len(l_five_cards) - 1):
		for index2 in range(index1 + 1,len(l_five_cards)):
			if l_five_cards[index1]['Number'] < l_five_cards[index2]['Number']:
				temp_card = l_five_cards[index1]
				l_five_cards[index1] = l_five_cards[index2]
				l_five_cards[index2] = temp_card
	return l_five_cards

#sorts given cards by ace-high order
def sort_cards_by_value(l_five_cards):
	global l_value_order
	for index1 in range(0,len(l_five_cards) - 1):
		for index2 in range(index1 + 1,len(l_five_cards)):
			if (l_value_order.index(l_five_cards[index1]['Value']) < l_value_order.index(l_five_cards[index2]['Value'])):
				temp_card = l_five_cards[index1]
				l_five_cards[index1] = l_five_cards[index2]
				l_five_cards[index2] = temp_card
	return l_five_cards

#sorts given cards by king-high order
def sort_cards_by_value1(l_five_cards):
	global l_value_order1
	for index1 in range(0,len(l_five_cards) - 1):
		for index2 in range(index1 + 1,len(l_five_cards)):
			if (l_value_order1.index(l_five_cards[index1]['Value']) < l_value_order1.index(l_five_cards[index2]['Value'])):
				temp_card = l_five_cards[index1]
				l_five_cards[index1] = l_five_cards[index2]
				l_five_cards[index2] = temp_card
	return l_five_cards

#reorders cards into order smallest to largest (ace-high)
def smallest_value_order(l_vals):
	global l_value_order
	small_val1 = l_value_order.index(l_vals[0]['Value'])
	for elem in l_vals:
		if l_value_order.index(elem['Value']) <= small_val1:
			small_val1 = l_value_order.index(elem['Value'])
	#print(l_value_order[small_val1])
	return l_value_order[small_val1]

#reorders cards into order smallest to largest (king-high)
def smallest_value_order1(l_vals):
	global l_value_order1
	small_val1 = l_value_order1.index(l_vals[0]['Value'])
	for elem in l_vals:
		if l_value_order1.index(elem['Value']) <= small_val1:
			small_val1 = l_value_order1.index(elem['Value'])
	#print(l_value_order[small_val1])
	return l_value_order1[small_val1]

#determines what hand each player has
def evaluate_cards():
	global community_cards
	global l_deck
	global l_results
	l_results = []
	count = 0
	for num in range(0,len(l_players)):
		player_result = {}
		if (betting_temp_player_list[num]['Folded?'] != True):
			player_result = {'Name' : betting_temp_player_list[num]['Name'],
							'Combination' : '',
							'Cards' : []}
			#print(l_players[num]['Name'] + ': ', end = " ")
			element = is_royal_flush(betting_temp_player_list[num])
			if element != []:
				real_element = sort_cards_by_value(element[0])
				player_result['Combination'] = 'Royal Flush'
				player_result['Cards'] = [real_element[0], real_element[1], real_element[2], real_element[3], real_element[4]]
				#print('Royal Flush (' + print_card(real_element[0]) + ', ' + print_card(real_element[1]) + ', ' + print_card(real_element[2]) + ', ' + print_card(real_element[3]) + ', ' + print_card(real_element[4]) + ')')		
			else:
				element = is_straight_flush(betting_temp_player_list[num])
				if element != []:
					real_element = sort_cards(element[0])
					player_result['Combination'] = 'Straight Flush'
					player_result['Cards'] = [real_element[0], real_element[1], real_element[2], real_element[3], real_element[4]]
					#print('Straight Flush (' + print_card(real_element[0]) + ', ' + print_card(real_element[1]) + ', ' + print_card(real_element[2]) + ', ' + print_card(real_element[3]) + ', ' + print_card(real_element[4]) + ')')
				else:
					element = is_four_of_a_kind(betting_temp_player_list[num])
					if element != []:
						real_element = element[0]
						player_result['Combination'] = 'Four of a Kind'
						player_result['Cards'] = [real_element[0], real_element[1], real_element[2], real_element[3]]
						#print('Four of a Kind (' + print_card(element[0][0]) + ', ' + print_card(element[0][1]) + ', ' + print_card(element[0][2]) + ', ' + print_card(element[0][3]) + ')')
					else:
						element = is_full_house(betting_temp_player_list[num])
						if element != []:
							real_element = full_house_sort(element[0])
							player_result['Combination'] = 'Full House'
							player_result['Cards'] = [real_element[0], real_element[1], real_element[2], real_element[3], real_element[4]]
							#print('Full House (' + print_card(real_element[0]) + ', ' + print_card(real_element[1]) + ', ' + print_card(real_element[2]) + ', ' + print_card(real_element[3]) + ', ' + print_card(real_element[4]) + ')')
						else:
							element = is_flush(betting_temp_player_list[num])
							if element != []:
								real_element = sort_cards_by_value(element[0])
								player_result['Combination'] = 'Flush'
								player_result['Cards'] = [real_element[0], real_element[1], real_element[2], real_element[3], real_element[4]]
								#print('Flush (' + print_card(real_element[0]) + ', ' + print_card(real_element[1]) + ', ' + print_card(real_element[2]) + ', ' + print_card(real_element[3]) + ', ' + print_card(real_element[4]) + ')')		
							else:
								element = is_straight(betting_temp_player_list[num])
								if element != []:
									real_element = sort_cards_by_value(element[0])
									player_result['Combination'] = 'Straight'
									player_result['Cards'] = [real_element[0], real_element[1], real_element[2], real_element[3], real_element[4]]
									#print('Straight (' + print_card(real_element[0]) + ', ' + print_card(real_element[1]) + ', ' + print_card(real_element[2]) + ', ' + print_card(real_element[3]) + ', ' + print_card(real_element[4]) + ')')
								else:
									element = is_straight1(betting_temp_player_list[num])
									if element != []:
										real_element = sort_cards_by_value1(element[0])
										player_result['Combination'] = 'Straight'
										player_result['Cards'] = [real_element[0], real_element[1], real_element[2], real_element[3], real_element[4]]
										#print('Straight (' + print_card(real_element[0]) + ', ' + print_card(real_element[1]) + ', ' + print_card(real_element[2]) + ', ' + print_card(real_element[3]) + ', ' + print_card(real_element[4]) + ')')
									else:
										element = is_three_of_a_kind(betting_temp_player_list[num])
										if element != []:
											real_element = element[0]
											player_result['Combination'] = 'Three of a Kind'
											player_result['Cards'] = [real_element[0], real_element[1], real_element[2], real_element[3], real_element[4]]
											#print('Three of a Kind (' + print_card(element[0][0]) + ', ' + print_card(element[0][1]) + ', ' + print_card(element[0][2]) + ')')
										else:
											element = is_two_pair(betting_temp_player_list[num])
											if element != []:
												player_result['Combination'] = 'Two Pair'
												player_result['Cards'] = [element[0], element[1], element[2], element[3], element[4]]
												#print('Two Pair (' + print_card(element[0][0]) + ', ' + print_card(element[0][1]) + ' and ' + print_card(element[1][0]) + ', ' + print_card(element[1][1]) + ')')
											else:
												element = is_one_pair(betting_temp_player_list[num])
												if element != []:
													player_result['Combination'] = 'One Pair'
													player_result['Cards'] = [element[0][0], element[0][1], element[0][2], element[0][3], element[0][4]]
													#print('One Pair (' + print_card(element[0][0]) + ', ' + print_card(element[0][1]) + ')')
												else:
													element = get_high_card(betting_temp_player_list[num])
													player_result['Combination'] = 'High Card'
													player_result['Cards'] = [element[0][0], element[0][1], element[0][2], element[0][3], element[0][4]]
													#print('High Card (' + print_card(element) + ')')
			l_results.append(player_result)
	return l_results

#rearrange hands in order if multiple people have same hand
def rearrange_hands(players):
	rearranged = []
	length = len(players)
	if players[0]['Combination'] == 'Royal Flush':
		rearranged = players
	elif players[0]['Combination'] == 'Straight Flush':
		while len(rearranged) != length:
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order1.index(players[i]['Cards'][0]['Value']) > l_value_order1.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)
	elif players[0]['Combination'] == 'Four of a Kind':
		while (len(rearranged) != length):
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order.index(players[i]['Cards'][0]['Value']) > l_value_order.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
					elif l_value_order.index(players[i]['Cards'][0]['Value']) == l_value_order.index(best_player['Cards'][0]['Value']):
						if l_value_order.index(players[i]['Cards'][4]['Value']) > l_value_order.index(best_player['Cards'][4]['Value']):
							best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)
	elif players[0]['Combination'] == 'Full House':
		while (len(rearranged) != length):
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order.index(players[i]['Cards'][0]['Value']) > l_value_order.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
					elif l_value_order.index(players[i]['Cards'][0]['Value']) == l_value_order.index(best_player['Cards'][0]['Value']):
						if l_value_order.index(players[i]['Cards'][3]['Value']) > l_value_order.index(best_player['Cards'][3]['Value']):
							best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)
	elif players[0]['Combination'] == 'Flush':
		while (len(rearranged) != length):
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order.index(players[i]['Cards'][0]['Value']) > l_value_order.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
					elif l_value_order.index(players[i]['Cards'][0]['Value']) == l_value_order.index(best_player['Cards'][0]['Value']):
						if l_value_order.index(players[i]['Cards'][1]['Value']) > l_value_order.index(best_player['Cards'][1]['Value']):
							best_player = players[i]
						elif l_value_order.index(players[i]['Cards'][1]['Value']) == l_value_order.index(best_player['Cards'][1]['Value']):
							if l_value_order.index(players[i]['Cards'][2]['Value']) > l_value_order.index(best_player['Cards'][2]['Value']):
								best_player = players[i]
							elif l_value_order.index(players[i]['Cards'][2]['Value']) == l_value_order.index(best_player['Cards'][2]['Value']):
								if l_value_order.index(players[i]['Cards'][3]['Value']) > l_value_order.index(best_player['Cards'][3]['Value']):
									best_player = players[i]
								elif l_value_order.index(players[i]['Cards'][3]['Value']) == l_value_order.index(best_player['Cards'][3]['Value']):
									if l_value_order.index(players[i]['Cards'][4]['Value']) > l_value_order.index(best_player['Cards'][4]['Value']):
										best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)
	elif players[0]['Combination'] == 'Straight':
		while len(rearranged) != length:
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order.index(players[i]['Cards'][0]['Value']) > l_value_order.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)
	elif players[0]['Combination'] == 'Three of a Kind':
		while len(rearranged) != length:
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order.index(players[i]['Cards'][0]['Value']) > l_value_order.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
					elif l_value_order.index(players[i]['Cards'][0]['Value']) == l_value_order.index(best_player['Cards'][0]['Value']):
						if l_value_order.index(players[i]['Cards'][3]['Value']) > l_value_order.index(best_player['Cards'][3]['Value']):
							best_player = players[i]
						elif l_value_order.index(players[i]['Cards'][3]['Value']) == l_value_order.index(best_player['Cards'][3]['Value']):
							if l_value_order.index(players[i]['Cards'][4]['Value']) > l_value_order.index(best_player['Cards'][4]['Value']):
								best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)
	elif players[0]['Combination'] == 'Two Pair':
		while len(rearranged) != length:
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order.index(players[i]['Cards'][0]['Value']) > l_value_order.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
					elif l_value_order.index(players[i]['Cards'][0]['Value']) == l_value_order.index(best_player['Cards'][0]['Value']):
						if l_value_order.index(players[i]['Cards'][2]['Value']) > l_value_order.index(best_player['Cards'][2]['Value']):
							best_player = players[i]
						elif l_value_order.index(players[i]['Cards'][2]['Value']) == l_value_order.index(best_player['Cards'][2]['Value']):
							if l_value_order.index(players[i]['Cards'][4]['Value']) > l_value_order.index(best_player['Cards'][4]['Value']):
								best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)
	elif players[0]['Combination'] == 'One Pair':
		while (len(rearranged) != length):
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order.index(players[i]['Cards'][0]['Value']) > l_value_order.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
					elif l_value_order.index(players[i]['Cards'][0]['Value']) == l_value_order.index(best_player['Cards'][0]['Value']):
						if l_value_order.index(players[i]['Cards'][2]['Value']) > l_value_order.index(best_player['Cards'][2]['Value']):
							best_player = players[i]
						elif l_value_order.index(players[i]['Cards'][2]['Value']) == l_value_order.index(best_player['Cards'][2]['Value']):
							if l_value_order.index(players[i]['Cards'][3]['Value']) > l_value_order.index(best_player['Cards'][3]['Value']):
								best_player = players[i]
							elif l_value_order.index(players[i]['Cards'][3]['Value']) == l_value_order.index(best_player['Cards'][3]['Value']):
								if l_value_order.index(players[i]['Cards'][4]['Value']) > l_value_order.index(best_player['Cards'][4]['Value']):
									best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)
	elif players[0]['Combination'] == 'High Card':
		while (len(rearranged) != length):
			if len(players) == 1:
				rearranged.append(players[0])
			else:
				best_player = players[0]
				for i in range(1, len(players)):
					if l_value_order.index(players[i]['Cards'][0]['Value']) > l_value_order.index(best_player['Cards'][0]['Value']):
						best_player = players[i]
					elif l_value_order.index(players[i]['Cards'][0]['Value']) == l_value_order.index(best_player['Cards'][0]['Value']):
						if l_value_order.index(players[i]['Cards'][1]['Value']) > l_value_order.index(best_player['Cards'][1]['Value']):
							best_player = players[i]
						elif l_value_order.index(players[i]['Cards'][1]['Value']) == l_value_order.index(best_player['Cards'][1]['Value']):
							if l_value_order.index(players[i]['Cards'][2]['Value']) > l_value_order.index(best_player['Cards'][2]['Value']):
								best_player = players[i]
							elif l_value_order.index(players[i]['Cards'][2]['Value']) == l_value_order.index(best_player['Cards'][2]['Value']):
								if l_value_order.index(players[i]['Cards'][3]['Value']) > l_value_order.index(best_player['Cards'][3]['Value']):
									best_player = players[i]
								elif l_value_order.index(players[i]['Cards'][3]['Value']) == l_value_order.index(best_player['Cards'][3]['Value']):
									if l_value_order.index(players[i]['Cards'][4]['Value']) > l_value_order.index(best_player['Cards'][4]['Value']):
										best_player = players[i]
				rearranged.append(best_player)
				players.remove(best_player)

	return rearranged

#determine the winner(s) of the hand
def determine_winner(l_player_stats):
	global l_hand_rankings

	hands_separation = [[],[],[],[],[],[],[],[],[],[]]
	final_l_player_stats = []
	
	for player in l_player_stats:
		hands_separation[l_hand_rankings.index(player['Combination'])].append(player)

	for players in hands_separation:
		if len(players) == 0:
			continue
		elif len(players) == 1:
			final_l_player_stats.append(players[0])
		else:
			rearranged = rearrange_hands(players)
			for player in rearranged:
				final_l_player_stats.append(player)
			
	print(' ')
	print('Sorted Rankings:')
	print()
	for element in final_l_player_stats:
		print(element['Name'] + ': ' + (' ' * (7 - (len(element['Name'])))), end = " ")
		print(element['Combination'] + (' ' * (16 - len(element['Combination']))), end = "")
		for card in element['Cards']:
			if ((element['Cards'].index(card) == len(element['Cards']) - 1)):
				print(print_card(card))
			else:
				print(print_card(card) + ',', end = " ")

	return final_l_player_stats

#adjust money based on special big blind and small blind scenarios
def adjust_money():
	global l_players
	global betting_temp_player_list
	global big_blind
	global small_blind
	global big_blind_amount
	global small_blind_amount

	for player in l_players:
		for player1 in betting_temp_player_list:
			if player['Name'] == player1['Name']:
				player['Money'] -= player1['Money']
				break

#move the dealer
def move_dealer():
	global dealer_order
	global player_count
	dealer_order = 0 if dealer_order >= len(l_players) - 1 else dealer_order + 1
	if (dealer_order > len(l_players) - 1):
		print("BAD2 " + str(dealer_order))

#print the player
def print_player_status():
	global l_players
	total = 0
	for player in l_players:
		if player['Money'] != 0:
			print(player['Name'] + ': ' + (' ' * (7 - len(player['Name']))) + str(player['Money']))
		if player['Money'] < 0:
			print('BAD3 ' + str(player['Money']))
		total += player['Money']
	return total

#play the full game
def play():
	global l_dealt_cards
	global l_players
	global dealer_order
	global player_count
	global l_deck
	global community_cards
	global big_blind
	global small_blind
	global big_blind_amount
	global small_blind_amount
	global betting_temp_player_list
	global human_players
	global folded_players
	global pot
	#deal_test_cards()
	#print_player_status()
	count = 1
	count1 = 0
	one_winner_flag = False
	dealer_moved = False
	temp_l_players = []
	skip_betting = False
	one_player_left = False
	return_list = []
	hand_count = 1
	first_hand_yes = True
	folded_players = []
	
	define_players()
	get_player_names()
	
	while one_winner_flag == False:
	#for hand_count in range(1,2):
		folded_players = []
		print('------------------------------------------------------------')
		print('------------------------------------------------------------')
		print('------------------------------------------------------------')
		print('Hand #' + str(count))
		if hand_count != 1:
			first_hand_yes = False
		#if hand_count == 1:
		#	assign_test_player_types()
		#else:
		#	assign_test_player_types1()
		#print_player_status()
		randomly_assign_player_types()
		#assign_test_player_types()
		community_cards = []
		l_deck = []
		make_deck()
		l_dealt_cards = []
		determine_blinds()
		#pot = determine_blind_amounts()
		dealer_moved = False
		print('BETTING ROUND 1')
		print()
		
		for player in l_players:
			if player['Order'] == small_blind:
				print(player['Name'] + ' = $' + str(small_blind_amount) + ' till now - small blind')
				break
		
		for player in l_players:
			if player['Order'] == big_blind:
				print(player['Name'] + ' = $' + str(big_blind_amount) + ' till now - big blind')
				break
			
		#deal_test_cards()
		deal_cards_to_players()
		#if hand_count == 1:
		#	deal_test_cards()
		#else:
		#	deal_test_cards1()
		make_temp_player_list()

		print()
		return_list = bet1(first_hand_yes)
		skip_betting = return_list[0]
		one_player_left = return_list[1]
		pot = get_current_pot()
		if pot < (big_blind_amount + small_blind_amount):
			print('BAD' + str(pot))
			pot = get_current_pot()
		#print('Pot: ' + str(pot))
		#print()
		if (skip_betting == False) and (one_player_left == False):
			print('------------------------------------------------------------')
			print('BETTING ROUND 2')
			deal_flop()
			make_temp_player_list2()
			return_list = bet2(first_hand_yes)
			skip_betting = return_list[0]
			one_player_left = return_list[1]
			#print()
			pot = get_current_pot()
			#print('Pot: ' + str(pot))
			if skip_betting == False and one_player_left == False:
				print('------------------------------------------------------------')
				print('BETTING ROUND 3')
				#print()
				deal_turn_or_river()
				clear_temp_list()
				return_list = bet3(first_hand_yes)
				skip_betting = return_list[0]
				one_player_left = return_list[1]
				#print()
				pot = get_current_pot()
				#print('Pot: ' + str(pot))
				if skip_betting == False and one_player_left == False:
					print('------------------------------------------------------------')
					print('BETTING ROUND 4')
					#print()
					deal_turn_or_river()
					clear_temp_list()
					return_list = bet4(first_hand_yes)
					skip_betting = return_list[0]
					one_player_left = return_list[1]
					#print()

		if len(community_cards) == 0:
			deal_flop()
			deal_turn_or_river()
			deal_turn_or_river()
		elif len(community_cards) == 3:
			deal_turn_or_river()
			deal_turn_or_river()
		elif len(community_cards) == 4:
			deal_turn_or_river()

		print('------------------------------------------------------------')
		pot = get_current_pot()
		print('Pot: ' + str(pot))
		print()
		print('Players:')
		print()
		#if (skip_betting == False):
		for player in l_players:
			if player['Name'] not in folded_players:
				print_player(player)
		print()
		
		print_community_cards()
		print()

		winner_order = determine_winner(evaluate_cards())
		
		winner_of_hand = ''
		
		for element in winner_order:
			for player in betting_temp_player_list:
				if (element['Name'] == player['Name']) and (player['Folded?'] != True):
					winner_of_hand = player['Name']
					break
			if winner_of_hand != '':
				break

		for player in l_players:
			if player['Name'] == winner_of_hand:
				player['Money'] += pot
				break
		print()
		print(winner_of_hand + ' has won ' + ' $' + str(pot) + '!')
		print()
		#Subtract amounts betted from players (special scenario for bb and sb)
		adjust_money()

		temp_l_players = []
		#determine the next dealer
		temp_dealer_order = dealer_order + 1
		while (l_players[temp_dealer_order]['Money'] == 0):
			temp_dealer_order += 1

		new_dealer_order = temp_dealer_order
		temp_l_players.append(l_players[new_dealer_order])

		for i in range(new_dealer_order + 1, len(l_players)):
			if l_players[i]['Money'] != 0:
				temp_l_players.append(l_players[i])

		for i in range(0, new_dealer_order):
			if l_players[i]['Money'] != 0:
				temp_l_players.append(l_players[i])

		if len(temp_l_players) == 1:
			one_winner_flag = True

		total = print_player_status()
		if total < 900:
			print('BAD2')
		print('Total: ' + str(total))
		print()
		print()
		print('Number of Hands Played: ' + str(count))
		print('------------------------------------------------------------')
		count += 1

		l_players = temp_l_players

		for i in range(0, len(l_players)):
			l_players[i]['Order'] = i

		input()

play()