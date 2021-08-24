from pubsub import pub

# Send messages to all listeners of topics
pub.sendMessage('football', arg={'headline': 'Ronaldo',
                                 'news': 'Sold for $1M'})
pub.sendMessage('chess', arg={'headline': 'AI',
                              'news': 'AlphaZero beats grandmaster Carlsen'})