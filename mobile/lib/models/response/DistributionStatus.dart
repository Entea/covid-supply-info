class DistributionStatus {
  final Status status;
  final String value;

  DistributionStatus(this.status, this.value);
}

enum Status { ready_to_sent, sent, delivered }
