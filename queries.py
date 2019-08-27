q_cpu = {
  "_source": [
    "system.cpu.idle.pct",
    "system.cpu.total.pct",
    "system.cpu.system.pct",
    "system.cpu.user.pct",
    "system.cpu.cores",
    "host.name",
    "@timestamp"],
  "sort": [
    {"@timestamp": {"order": "asc"}}
  ],
  "query": {
    "bool": {
      "must": [
        {"match": {"event.module": "system"}},
        {"match": {"metricset.name": "cpu"}},
        {"match": {"host.name": "node"}}
      ],
      "filter": {
        "range" : {
          "@timestamp" : {
            "gte": "now-1d/d",
            "lt": "now/d"
          }
        }
      }
    }
  }
}

q_load = {
  "_source": [
    "system.load.1",
    "system.load.5",
    "system.load.15",
    "host.name",
    "@timestamp"],
  "sort": [
    {"@timestamp": {"order": "asc"}}
  ],
  "query": {
    "bool": {
      "must": [
        {"match": {"event.module": "system"}},
        {"match": {"metricset.name": "load"}},
        {"match": {"host.name": "node"}}
      ],
      "filter": {
        "range" : {
          "@timestamp" : {
            "gte": "now-1h/h",
            "lt": "now/h"
          }
        }
      }
    }
  }
}

q_memory = {
  "_source": [
    "system.memory.actual.used.pct",
    "system.memory.swap.used.pct",
    "system.memory.used.pct",
    "host.name",
    "@timestamp"],
  "sort": [
    {"@timestamp": {"order": "asc"}}
  ],
  "query": {
    "bool": {
      "must": [
        {"match": {"event.module": "system"}},
        {"match": {"metricset.name": "memory"}},
        {"match": {"host.name": "node"}}
      ],
      "filter": {
        "range" : {
          "@timestamp" : {
            "gte": "now-1d/d",
            "lt": "now/d"
          }
        }
      }
    }
  }
}

q_fs = {
  "_source": [
    "system.filesystem.total",
    "system.filesystem.free",
    "system.filesystem.used.bytes",
    "system.filesystem.used.pct",
    "system.filesystem.mount_point",
    "system.filesystem.device_name",
    "host.name",
    "@timestamp"],
  "sort": [
    {"@timestamp": {"order": "asc"}}
  ],
  "query": {
    "bool": {
      "must": [
        {"match": {"event.module": "system"}},
        {"match": {"metricset.name": "filesystem"}},
        {"match": {"host.name": "node"}}
      ],
      "filter": {
        "range" : {
          "@timestamp" : {
            "gte": "now-1d/d",
            "lt": "now/d"
          }
        }
      }
    }
  }
}

q_diskio = {
  "_source": [
    "system.diskio.iostat.read.await",
    "system.diskio.iostat.read.per_sec.bytes",
    "system.diskio.iostat.write.await",
    "system.diskio.iostat.write.per_sec.bytes",
    "system.diskio.name",
    "host.name",
    "@timestamp"],
  "sort": [
    {"@timestamp": {"order": "asc"}}
  ],
  "query": {
    "bool": {
      "must": [
        {"match": {"event.module": "system"}},
        {"match": {"metricset.name": "diskio"}},
        {"match": {"host.name": "node"}}
      ],
      "filter": {
        "range" : {
          "@timestamp" : {
            "gte": "now-1h/h",
            "lt": "now/h"
          }
        }
      }
    }
  }
}