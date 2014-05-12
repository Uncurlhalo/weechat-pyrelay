import relay
import weechatObjects as objs

# TODO: Complete implementation of all the sync replies

def processReply(reply, buffers):
	# this will take the reply, look at is ID field, and take some action based on its type
	# these actions will all update weechat datastructures from weechatObjects.
	options = {	'_pong' : pong,
				'_upgrade' : upgrade,
				'_nicklist' : nicklist,
				'_buffer_moved' : bufMoved,
				'_buffer_merged' : bufMerged,
				'_buffer_opened' : bufOpened,
				'_buffer_hidden' : bufHidden,
				'_buffer_closing' : bufClosing,
				'_buffer_renamed' : bufRenamed,
				'_nicklist_diff' : nicklistDiff,
				'_upgrade_ended' : upgradeEnded,
				'_buffer_unmerged' : bufUnmerged,
				'_buffer_unhidden' : bufUnhidden,
				'_buffer_line_added' : bufLineAdded,
				'_buffer_type_changed' : bufTypeChanged,
				'_buffer_localvar_added' : bufLocVarAdded,
				'_buffer_title_changed' : bufTitleChanged,
				'_buffer_localvar_changed' : bufLocVarChanged,
				'_buffer_localvar_removed' : bufLocVarRemoved
				}
	msgID = reply.msgid
	ret = options[msgID](reply, buffers)
	return ret

def pong(reply, buffers):
	print("Ponged")

def upgrade(reply, buffers):
	print("upgraded")

def nicklist(reply, buffers):
	print("nicklist")

def bufMoved(reply, buffers):
	print("buffer moved")

def bufMerged(reply, buffers):
	print("buffer merged")

def bufOpened(reply, buffers):
	print("buffer opened")

def bufHidden(reply, buffers):
	print("buffer hidden")

def bufClosing(reply, buffers):
	print("buffer closing")

def bufRenamed(reply, buffers):
	print("buffer renamed")

def nicklistDiff(reply, buffers):
	print("nicklist diff")

def upgradeEnded(reply, buffers):
	print("upgrade ended")

def bufUnmerged(reply, buffers):
	print("buffer unmerged")

def bufUnhidden(reply, buffers):
	print("buffer unhidden")

def bufLineAdded(reply, buffers):
	print("buffer line added")
	replyItems = reply.objects[0].value['items'][0]
	for key,buf in buffers.items():
		if buf.path == replyItems['buffer']:
			displayed = bool(replyItems['displayed'])
			message = replyItems['message']
			prefix = replyItems['prefix']
			date = replyItems['date']
			buf.lines.append(objs.WeechatLine(message, date, prefix, displayed))
			return True
	return False

def bufTypeChanged(reply, buffers):
	print("buffer type changed")

def bufLocVarAdded(reply, buffers):
	print("buffer local var added")

def bufTitleChanged(reply, buffers):
	print("buffer title changed")
	return True

def bufLocVarChanged(reply, buffers):
	print("buffer local var changed")
	return False

def bufLocVarRemoved(reply, buffers):
	print("buffer local var removed")