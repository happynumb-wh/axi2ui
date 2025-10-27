class axiIdAllocator():
    def __init__(self, axiIdWidth):
        self.axiIdWidth = axiIdWidth
        self.max_id = 2**axiIdWidth
        
        self.raddr_to_id = {}  # 读地址到ID的映射
        self.waddr_to_id = {}  # 写地址到ID的映射
        self.raddr_to_id_ref_count = {}  # 读地址到ID映射的引用计数
        self.waddr_to_id_ref_count = {}  # 写地址到ID映射的引用计数
        
        self.used_rid = set()  # 已使用的读ID集合
        self.used_wid = set()  # 已使用的写ID集合
        self.rid_ref_count = {}  # 读ID的引用计数
        self.wid_ref_count = {}  # 写ID的引用计数
        
        # 下一个可用的最小ID
        self.next_rid = 0
        self.next_wid = 0

    def _find_next_available_id(self, used_ids, next_id):
        """找到下一个可用的最小ID"""
        start_id = next_id
        while True:
            if next_id not in used_ids:
                return next_id
            next_id = (next_id + 1) % self.max_id
            if next_id == start_id:  # 如果转了一圈还没找到，返回0
                return 0

    def allocWriteId(self, addr):
        """分配写ID"""
        # return 0
        # self.next_wid = (self.next_wid + 1) % 32
        # return self.next_wid
        
        
        # 如果该地址已有分配的ID，增加引用计数并返回
        if addr in self.waddr_to_id:
            id = self.waddr_to_id[addr]
            self.wid_ref_count[id] += 1
            if (addr, id) not in self.waddr_to_id_ref_count:
                print("[allocWriteId error] addr has alloc wid, but (addr, id) ref not found")
            self.waddr_to_id_ref_count[(addr, id)] += 1
            return id
            
        # 找到下一个可用的最小ID
        new_id = self._find_next_available_id(self.used_wid, self.next_wid)
        
        # 更新映射和已使用ID集合
        self.waddr_to_id[addr] = new_id
        self.used_wid.add(new_id)
        self.wid_ref_count[new_id] = 1  # 初始化引用计数
        self.waddr_to_id_ref_count[(addr, new_id)] = 1
        
        # 更新下一个可用ID
        self.next_wid = (new_id + 1) % self.max_id
        
        return new_id

    def allocReadId(self, addr):
        """分配读ID"""
        # return 0
        # self.next_rid = (self.next_rid + 1) % 32
        # return self.next_rid
        
        
        # 如果该地址已有分配的ID，增加引用计数并返回
        if addr in self.raddr_to_id:
            id = self.raddr_to_id[addr]
            self.rid_ref_count[id] += 1
            if (addr, id) not in self.raddr_to_id_ref_count:
                print("[allocReadId error] addr has alloc rid, but (addr, id) ref not found")
            self.raddr_to_id_ref_count[(addr, id)] += 1
            return id
            
        # 找到下一个可用的最小ID
        new_id = self._find_next_available_id(self.used_rid, self.next_rid)
        
        # 更新映射和已使用ID集合
        self.raddr_to_id[addr] = new_id
        self.used_rid.add(new_id)
        self.rid_ref_count[new_id] = 1  # 初始化引用计数
        self.raddr_to_id_ref_count[(addr, new_id)] = 1
        
        # 更新下一个可用ID
        self.next_rid = (new_id + 1) % self.max_id
        
        return new_id
    
    def releaseWriteId(self, addr, id):
        # return
        
        
        """释放写ID"""
        if addr in self.waddr_to_id:
            if self.waddr_to_id[addr] != id:
                print("[releaseWriteId error] release wid and addr not match")
            if (addr, id) not in self.waddr_to_id_ref_count:
                print("[releaseWriteId error] release wid and addr not match (addr, id) ref not found)")
            
            # 减少引用计数
            self.wid_ref_count[id] -= 1
            self.waddr_to_id_ref_count[(addr, id)] -= 1
            
            # 如果引用计数为0，才真正释放ID
            if self.waddr_to_id_ref_count[(addr, id)] == 0:
                del self.waddr_to_id[addr]
                del self.waddr_to_id_ref_count[(addr, id)]
            if self.wid_ref_count[id] == 0:
                self.used_wid.discard(id)
                del self.wid_ref_count[id]
                # 如果释放的ID比当前next_wid小，更新next_wid
                if id < self.next_wid:
                    self.next_wid = id
        else:
            print("[releaseWriteId error] release wid and addr not match (addr not in waddr_to_id)")
    
    def releaseReadId(self, addr, id):
        # return
        
        
        """释放读ID"""
        if addr in self.raddr_to_id:
            if self.raddr_to_id[addr] != id:
                print("[releaseReadId error] release rid and addr not match")
            if (addr, id) not in self.raddr_to_id_ref_count:
                print("[releaseReadId error] release rid and addr not match (addr, id) ref not found)")
            
            # 减少引用计数
            self.rid_ref_count[id] -= 1
            self.raddr_to_id_ref_count[(addr, id)] -= 1
            
            # 如果引用计数为0，才真正释放ID
            if self.raddr_to_id_ref_count[(addr, id)] == 0:
                del self.raddr_to_id[addr]
                del self.raddr_to_id_ref_count[(addr, id)]
            if self.rid_ref_count[id] == 0:
                self.used_rid.discard(id)
                del self.rid_ref_count[id]
                # 如果释放的ID比当前next_rid小，更新next_rid
                if id < self.next_rid:
                    self.next_rid = id
        else:
            print("[releaseReadId error] release rid and addr not match (addr not in raddr_to_id)")
