# connect_result = self.input.connect("Sample Warehouse")
# if connect_result.status != "ok":
#   print(connect_result.message)

# transfer = self.input.take(fragment_id, 1)
# if transfer.status == "ok":
#   loaded = self.load(fragment_id)

# start = self.chamber.glow
# target = get_component("bio_exchange_1").active_order().target_glow
# sig_r = self.lamp_signature("red")
# sig_g = self.lamp_signature("green")
# sig_b = self.lamp_signature("blue")
# # Solve start + r*sig_r + g*sig_g + b*sig_b == target.
# lamps = self.set_lamps(r, g, b)

# if lamps.status == "ok" and self.glow() == target:
#   infusion = self.infuse()
#   if infusion.status != "ok":
#     print(infusion.message)





# print(self.input.take(self.input.stacks()[0].id,1))

# self.load(self.input.stacks()[0].id)


# self.output.connect("bio_exchange_2")
# # print(self.chamber.fragment_id)
# # self.infuse()
# print(self.output.stacks())
# self.output.send(self.output.stacks()[0].id,self.output.stacks()[0].count)


self.input.flush()
