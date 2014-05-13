import relay
import weechatObjects as objs

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
	return False

def nicklist(reply, buffers):
	print("sync message: nicklist")
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
		else:
			pass
	return True

def bufMoved(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufMerged(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufOpened(reply, buffers):
	print("sync message: buffer opened")
	replyItems = reply.objects[0].value['items'][0]
	full_name = replyItems['full_name']
	short_name = replyItems['short_name']
	path = replyItems['__path'][0]
	title = replyItems['title']
	buffers[full_name] = objs.WeechatBuffer(path, full_name, short_name, title)
	return True

def bufHidden(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufClosing(reply, buffers):
	print("sync message: buffer closing")
	return True

def bufRenamed(reply, buffers):
	print("sync message: buffer renamed")
	replyItems = reply.objects[0].value['items'][0]
	for key,buf in buffers.items():
		if buf.path == replyItems['__path']:
			full_name = replyItems['full_name']
			short_name = replyItems['short_name']
			buf.full_name = full_name
			buf.short_name = short_name
	return True

def nicklistDiff(reply, buffers):
	# Not needed currently, implement when needed
	# this currently only indicates that a nicks group has changed of a group has changed order with parents, so for now it isnt needed
	# since this data isnt tracked by our nick datastructure
	return False

def upgradeEnded(reply, buffers):

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
			buf.getPrefixWidth()
		else:
			pass
	return True

def bufTypeChanged(reply, buffers):
	# Not needed currently, implement when needed
	print("buffer type changed")
	return True

def bufLocVarAdded(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufTitleChanged(reply, buffers):
	print("sync message: buffer title changed")
	replyItems = reply.objects[0].value['items'][0]
	for key,buf in buffers.items():
		if buf.path == replyItems['__path']:
			buf.title = replyItems['title']
	return True

def bufLocVarChanged(reply, buffers):
	# Not needed currently, implement when needed
	return False

def bufLocVarRemoved(reply, buffers):
	# Not needed currently, implement when needed
	return False