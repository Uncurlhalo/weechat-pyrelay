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
	# Not needed currently, implement when needed
	return False

def upgrade(reply, buffers):
	# Not needed currently, implement when needed
	return True

def nicklist(reply, buffers):
	nicklist = objs.WeechatNickList()
	nicksItems = reply.objects[0].value['items']
	for key,buf in buffers.items():
		if buf.path == nicksItems['buffers']:
			for item in nicksItems:
				if item['group']:
					pass
				else:
					name = item['name']
					prefix = item['prefix']
					color = item['color']
					visible = bool(item['visible'])
					nicklist.addNick(objs.WeechatNick(name, prefix, color, visible))
			buf.nicklist = nicklist
			return True
		else:
			pass
	return False

def bufMoved(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufMerged(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufOpened(reply, buffers):
	# Not needed currently, implement when needed
	return True

def bufHidden(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufClosing(reply, buffers):
	# Not needed currently, implement when needed
	return True

def bufRenamed(reply, buffers):
	replyItems = reply.objects[0].value['items'][0]
	for key,buf in buffers.items():
		if buf.path == replyItems['buffer']:
			full_name = replyItems['full_name']
			short_name = replyItems['short_name']
			buf.full_name = full_name
			buf.short_name = short_name
	return True

def nicklistDiff(reply, buffers):
	nicksItems = reply.objects[0].value['items'][0]
	for key,buf in buffers.items():
		if buf.path == nicksItems['buffer']:
			for item in nicksItems:
				if item['group']:
					pass
				else:
					# TODO: figure how to find the nick already in the list and only make the changes given by the diff
					# since the diff can just changes things like group/prefix, we shouldnt need to add a new nick, just
					# change the values of a nick already there.
					pass
	return True

def upgradeEnded(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufUnmerged(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufUnhidden(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufLineAdded(reply, buffers):
	replyItems = reply.objects[0].value['items'][0]
	for key,buf in buffers.items():
		if buf.path == replyItems['buffer']:
			displayed = bool(replyItems['displayed'])
			message = replyItems['message']
			prefix = replyItems['prefix']
			date = replyItems['date']
			buf.lines.append(objs.WeechatLine(message, date, prefix, displayed))
		else:
			pass
	return True

def bufTypeChanged(reply, buffers):
	# Not needed currently, implement when needed
	print("buffer type changed")
	# likely will have something UI-wise change
	return True

def bufLocVarAdded(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufTitleChanged(reply, buffers):
	replyItems = reply.objects[0].value['items'][0]
	for key,buf in buffers.items():
		if buf.path == replyItems['buffer']:
			buf.title = replyItems['title']
	return True

def bufLocVarChanged(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufLocVarRemoved(reply, buffers):
	# Not needed currently, implement when needed
	return False